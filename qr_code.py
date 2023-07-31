import openpyxl
import qrcode
import os
import re

def sanitize_filename(filename):
    # Rimuove caratteri speciali e spazi dal nome del file
    return re.sub(r'[^\w\-_. ]', '', filename)

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(filename)

def process_invitations(input_file, output_folder):
    workbook = openpyxl.load_workbook(input_file)
    sheet = workbook.active

    # Rileva i dati delle colonne C (numero nella lista) e D (nome)
    positions = [cell[0].value for cell in sheet["C7:C158"]]
    names = [cell[0].value for cell in sheet["D7:D158"]]

    # Creazione della cartella di destinazione se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for position, name in zip(positions, names):
        # Rimuove caratteri speciali dal nome del partecipante
        sanitized_name = sanitize_filename(name)
        image_filename = os.path.join(output_folder, f"{sanitized_name}.png")
        qr_data = f"Nome: {name}, Numero nella lista: {position}"

        generate_qr_code(qr_data, image_filename)
        print(f"Generato QR per {name}, numero {position}")

if __name__ == "__main__":
    input_file = input("Inserisci il percorso del file Excel di input: ")
    output_folder = input("Inserisci il percorso della cartella di destinazione dei codici QR: ")

    process_invitations(input_file, output_folder)
