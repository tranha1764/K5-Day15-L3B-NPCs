import type { ChatResponse } from "../../types";
import { formatVnd } from "../../utils/format";
import { Card } from "../common/Card";
import { KeyValueList } from "../common/KeyValueList";
import { OrderItemsTable } from "./OrderItemsTable";
import styles from "./Sidebar.module.css";

/** Thẻ "Đơn hàng" — dữ liệu server đọc từ data/orders.json để khách / CSKH đối chiếu. */
export function OrderCard({ response }: { response: ChatResponse | null }) {
  const order = response?.order;
  if (!order) {
    const msg = !response
      ? "Chưa tra đơn nào."
      : response.order_id
        ? `Không tìm thấy đơn ${response.order_id} trong dữ liệu.`
        : "Tin nhắn chưa có mã đơn.";
    return (
      <Card title="Đơn hàng">
        <p className={styles.placeholder}>{msg}</p>
      </Card>
    );
  }
  return (
    <Card title="Đơn hàng">
      <KeyValueList
        rows={[
          { label: "Mã đơn", value: order.order_id },
          { label: "Quán", value: order.restaurant_name ?? "—" },
          { label: "Trạng thái", value: order.status ?? "—" },
          { label: "Trễ", value: order.delay_minutes != null ? `${order.delay_minutes} phút` : "—" },
          { label: "Thanh toán", value: order.payment_method ?? "—" },
          { label: "Tổng", value: formatVnd(order.total_vnd) },
        ]}
      />
      <OrderItemsTable items={order.items ?? []} />
      <p className={styles.note}>Dữ liệu đơn giả lập (data/orders.json).</p>
    </Card>
  );
}
