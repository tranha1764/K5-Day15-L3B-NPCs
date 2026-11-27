import { ChatPanel } from "./components/chat/ChatPanel";
import { FakeModeBanner } from "./components/layout/FakeModeBanner";
import { Header } from "./components/layout/Header";
import { Sidebar } from "./components/sidebar/Sidebar";
import { useChat } from "./hooks/useChat";
import { isFakeMode } from "./utils/format";
import styles from "./App.module.css";

export default function App() {
  const { messages, latest, busy, send, reset } = useChat();

  return (
    <>
      <Header onReset={reset} canReset={messages.length > 0} />
      <FakeModeBanner visible={isFakeMode(latest?.trace)} />
      <main className={styles.layout}>
        <ChatPanel messages={messages} busy={busy} onSend={send} />
        <Sidebar latest={latest} />
      </main>
    </>
  );
}
