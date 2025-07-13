import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

def plot_feasible_region(A, b, optimal):
    x1 = np.linspace(0, max(b)*1.5, 400)

    # Hitung nilai x2 untuk setiap kendala: a11*x1 + a12*x2 <= b1 -> x2 <= (b1 - a11*x1) / a12
    y1 = (b[0] - A[0][0]*x1) / A[0][1]
    y2 = (b[1] - A[1][0]*x1) / A[1][1]
    y3 = (b[2] - A[2][0]*x1) / A[2][1]

    # Plot garis kendala
    plt.figure(figsize=(8,6))
    plt.plot(x1, y1, label='Waktu Mesin')
    plt.plot(x1, y2, label='Bahan Baku')
    plt.plot(x1, y3, label='Tenaga Kerja')

    # Area feasible
    y_min = np.minimum(np.minimum(y1, y2), y3)
    y_min = np.maximum(y_min, 0)  # batas bawah 0
    plt.fill_between(x1, 0, y_min, color='grey', alpha=0.3)

    # Titik solusi optimal
    plt.plot(optimal[0], optimal[1], 'ro', label='Solusi Optimal')

    plt.xlim(0, max(x1))
    plt.ylim(0, max(y_min)*1.1)
    plt.xlabel('Jumlah Produk 1')
    plt.ylabel('Jumlah Produk 2')
    plt.title('Area Feasible dan Solusi Optimal')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    print("=== Optimasi Produksi Linear Programming ===")

    # Input keuntungan
    c1 = float(input("Keuntungan per unit produk 1: "))
    c2 = float(input("Keuntungan per unit produk 2: "))

    # Input batasan sumber daya
    print("\nMasukkan konsumsi sumber daya per unit produk:")
    a11 = float(input("Waktu mesin produk 1 (jam): "))
    a12 = float(input("Waktu mesin produk 2 (jam): "))

    a21 = float(input("Bahan baku produk 1 (unit): "))
    a22 = float(input("Bahan baku produk 2 (unit): "))

    a31 = float(input("Tenaga kerja produk 1 (jam): "))
    a32 = float(input("Tenaga kerja produk 2 (jam): "))

    b1 = float(input("\nBatas maksimum waktu mesin (jam): "))
    b2 = float(input("Batas maksimum bahan baku (unit): "))
    b3 = float(input("Batas maksimum tenaga kerja (jam): "))

    c = [-c1, -c2]  # linprog minimization
    A = [
        [a11, a12],
        [a21, a22],
        [a31, a32]
    ]
    b = [b1, b2, b3]

    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))

    if res.success:
        print("\nSolusi Optimal:")
        print(f"Jumlah produk 1: {res.x[0]:.2f}")
        print(f"Jumlah produk 2: {res.x[1]:.2f}")
        print(f"Keuntungan maksimal: {-res.fun:.2f}")
        plot_feasible_region(A, b, res.x)
    else:
        print("Tidak ditemukan solusi optimal.")

if __name__ == "__main__":
    main()
