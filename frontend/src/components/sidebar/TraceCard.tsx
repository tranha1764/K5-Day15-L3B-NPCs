import type { TraceSummary } from "../../types";
import { formatModels } from "../../utils/format";
import { Card } from "../common/Card";
import { KeyValueList } from "../common/KeyValueList";
import styles from "./Sidebar.module.css";

/** Thẻ "Trace lượt gần nhất" — model, số lần gọi, token (lấy từ tracing.end() phía server). */
export function TraceCard({ trace }: { trace: TraceSummary | null }) {
  if (!trace) {
    return (
      <Card title="Trace lượt gần nhất">
        <p className={styles.placeholder}>—</p>
      </Card>
    );
  }
  return (
    <Card title="Trace lượt gần nhất">
      <KeyValueList
        rows={[
          { label: "Model", value: formatModels(trace.models) },
          { label: "Gọi model", value: `${trace.model_calls} lần` },
          { label: "Gọi công cụ", value: `${trace.tool_calls} lần` },
          { label: "Token vào / ra", value: `${trace.tokens_in} / ${trace.tokens_out}` },
          { label: "Thời gian", value: `${trace.latency_s}s` },
        ]}
      />
      {trace.errors.length > 0 && (
        <ul className={styles.errors}>
          {trace.errors.map((e, i) => (
            <li key={i}>{e}</li>
          ))}
        </ul>
      )}
    </Card>
  );
}
