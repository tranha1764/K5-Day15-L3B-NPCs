import type { OrderItem } from "../../types";
import { formatVnd } from "../../utils/format";
import styles from "./Sidebar.module.css";

export function OrderItemsTable({ items }: { items: OrderItem[] }) {
  if (!items.length) return null;
  return (
    <table className={styles.items}>
      <tbody>
        {items.map((it, i) => (
          <tr key={it.item_id ?? `${it.name}-${i}`}>
            <td>
              {it.qty ?? 1} × {it.name}
            </td>
            <td className={styles.num}>{formatVnd(it.price_vnd)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
