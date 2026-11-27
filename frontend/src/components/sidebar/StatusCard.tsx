import { getStatusInfo } from "../../constants/status";
import type { ChatResponse } from "../../types";
import { Card } from "../common/Card";
import { DraftDetails } from "./DraftDetails";
import styles from "./Sidebar.module.css";

/** Thẻ "Trạng thái xử lý": xanh (draft_ready) · vàng (need_info) · đỏ (escalated / rejected) · xám (chưa có). */
export function StatusCard({ response }: { response: ChatResponse | null }) {
  if (!response) {
    return (
      <Card title="Trạng thái xử lý">
        <p className={styles.placeholder}>Chưa có tin nhắn.</p>
      </Card>
    );
  }
  if (response.error) {
    return (
      <Card title="Trạng thái xử lý">
        <div className={`${styles.statusBox} tone-bad`}>
          <strong>Lỗi khi chạy answer()</strong>
          <span>{response.error}</span>
        </div>
      </Card>
    );
  }
  const info = getStatusInfo(response.status);
  return (
    <Card title="Trạng thái xử lý">
      <div className={`${styles.statusBox} tone-${info.tone}`}>
        <strong>{info.title}</strong>
        <span>{info.hint}</span>
      </div>
      {response.draft && <DraftDetails draft={response.draft} />}
    </Card>
  );
}
