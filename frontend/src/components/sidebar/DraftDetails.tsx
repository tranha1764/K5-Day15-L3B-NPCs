import { ACTION_LABEL } from "../../constants/status";
import type { ResolutionDraft } from "../../types";
import { formatVnd } from "../../utils/format";
import { KeyValueList } from "../common/KeyValueList";
import styles from "./Sidebar.module.css";

/** Chi tiết bản nháp hoàn tiền / voucher / chuyển CSKH — luôn kèm câu nhắc "chưa thực hiện". */
export function DraftDetails({ draft }: { draft: ResolutionDraft }) {
  return (
    <div className={styles.section}>
      <KeyValueList
        rows={[
          { label: "Hành động", value: ACTION_LABEL[draft.action] ?? draft.action ?? "—" },
          { label: "Số tiền", value: formatVnd(draft.amount_vnd) },
          { label: "Lý do", value: draft.reason || "—" },
        ]}
      />
      <p className={styles.note}>Bản nháp — chưa thực hiện. Chỉ CSKH bấm duyệt mới hoàn tiền / phát voucher.</p>
    </div>
  );
}
