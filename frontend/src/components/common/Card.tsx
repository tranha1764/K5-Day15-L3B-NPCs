import type { ReactNode } from "react";
import styles from "./Card.module.css";

interface CardProps {
  title?: string;
  children: ReactNode;
  className?: string;
}

/** Khung thẻ có tiêu đề nhỏ — dùng cho các thẻ ở cột bên phải. */
export function Card({ title, children, className }: CardProps) {
  return (
    <section className={[styles.card, className].filter(Boolean).join(" ")}>
      {title && <h2 className={styles.title}>{title}</h2>}
      {children}
    </section>
  );
}
