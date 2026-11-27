"""Đếm số liệu từ bảng review công khai đã gắn nhãn (evidence/reviews_labeled.csv).

Chỉ dùng thư viện chuẩn của Python để người ngoài nhóm chạy lại ra đúng cùng con số.
Cách chạy:
    python evidence/count_reviews.py
"""
import csv
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "reviews_labeled.csv")


def main():
    by_app = defaultdict(list)
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            by_app[row["app"]].append(row)

    print("App         | N   | 1-3*      | Tre/ghep    | Sai/thieu/mat | CSKH/hoan tien (Bot/AI) | >=1 van de")
    print("-" * 98)

    tot_n = tot_neg = tot_tre = tot_sai = tot_cskh = tot_bot = tot_any = 0
    for app in ("ShopeeFood", "Grab", "Be"):
        rows = by_app[app]
        n = len(rows)
        neg = sum(1 for r in rows if int(r["rating"]) <= 3)
        tre = sum(1 for r in rows if r["tre_ghep"] == "1")
        sai = sum(1 for r in rows if r["sai_thieu_mat"] == "1")
        cskh = sum(1 for r in rows if r["cskh_hoan_tien"] == "1")
        bot = sum(1 for r in rows if r["bot_ai"] == "1")
        any_p = sum(
            1 for r in rows
            if r["tre_ghep"] == "1" or r["sai_thieu_mat"] == "1" or r["cskh_hoan_tien"] == "1"
        )
        print(
            f"{app:<11} | {n:<3} | {neg:>2}/{n} ({neg*100/n:4.1f}%) | "
            f"{tre:>2}/{n} ({tre*100/n:4.1f}%) | {sai:>2}/{n} ({sai*100/n:4.1f}%)   | "
            f"{cskh:>2}/{n} ({cskh*100/n:4.1f}%) (bot {bot})   | {any_p:>2}/{n} ({any_p*100/n:4.1f}%)"
        )
        tot_n += n
        tot_neg += neg
        tot_tre += tre
        tot_sai += sai
        tot_cskh += cskh
        tot_bot += bot
        tot_any += any_p

    print("-" * 98)
    print(
        f"{'TONG':<11} | {tot_n:<3} | {tot_neg:>3}/{tot_n} ({tot_neg*100/tot_n:4.1f}%) | "
        f"{tot_tre:>2}/{tot_n} ({tot_tre*100/tot_n:4.1f}%) | {tot_sai:>2}/{tot_n} ({tot_sai*100/tot_n:4.1f}%)   | "
        f"{tot_cskh:>2}/{tot_n} ({tot_cskh*100/tot_n:4.1f}%) (bot {tot_bot})  | {tot_any:>3}/{tot_n} ({tot_any*100/tot_n:4.1f}%)"
    )


if __name__ == "__main__":
    main()
