# Tính giá trị đa thức bằng Horner và phương pháp lặp

Ứng dụng web tính giá trị đa thức bậc 5

`f(x) = a1*x^5 + a2*x^4 + a3*x^3 + a4*x^2 + a5*x + a6`

bằng hai phương pháp:

- Lặp trực tiếp qua từng hạng tử.
- Sơ đồ Horner với công thức `b[k] = b[k-1] * x + a[k]`.

## Chạy trên máy

Mở trực tiếp tệp `index.html` bằng trình duyệt. Dự án không cần cài đặt thư viện.
## Ứng dụng Windows

- Chạy bằng Python: `python horner_calculator.py`.
- Tạo file chạy độc lập: mở `build_windows.bat`.
- File sau khi build nằm tại `dist/HornerCalculator.exe` và không yêu cầu máy nhận cài Python.

GitHub Actions cũng tự động tạo artifact `HornerCalculator-Windows` mỗi khi mã Python được cập nhật trên nhánh `main`.

