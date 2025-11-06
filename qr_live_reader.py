import cv2
from pyzbar import pyzbar
import imutils

def read_qr_codes(frame):
    """
    Detecta y decodifica códigos QR en la imagen.
    """
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Decodificar información
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        text = f"{barcode_data} ({barcode_type})"
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return frame, [b.data.decode("utf-8") for b in barcodes]


def main():
    # --- CONFIGURACIÓN DE CÁMARA ---
    # Para webcam local: usa 0 o 1
    # Para cámara IP: cambia por la URL del stream (rtsp/http)
    CAMERA_SOURCE = "rtsp://admin:admin123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0" # o "rtsp://usuario:contraseña@192.168.x.x:554/stream"

    cap = cv2.VideoCapture(CAMERA_SOURCE)

    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara.")
        return

    print("✅ Cámara iniciada. Presiona 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar frame")
            break

        frame = imutils.resize(frame, width=800)
        frame, codes = read_qr_codes(frame)

        # Mostrar resultados
        cv2.imshow("Detección de QR", frame)

        if codes:
            print(f"📦 Códigos detectados: {codes}")

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
