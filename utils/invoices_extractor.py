import os
import glob
import zipfile
import xmltodict
from pyexpat import ExpatError
from .settings import handle_empty, REGISTER_EMAIL, TEMP_PATH
from .files_organizer import load_new_invoices


def clean_data():
    files = glob.glob(os.path.join(TEMP_PATH, "*"))
    for file in files:
        os.remove(file)


def unzip(path):
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(TEMP_PATH)


def find_xml():
    file_pattern = "*.xml"

    files = glob.glob(os.path.join(TEMP_PATH, file_pattern))
    if not files:
        files = glob.glob(os.path.join(TEMP_PATH, file_pattern.upper()))
    for f in files:
        with open(f, "r", encoding='utf-8') as xml:
            try:
                xml_data = xml.read()
                data_dict = xmltodict.parse(xml_data)
                if "FacturaElectronica" in data_dict.keys():
                    return data_dict
            except ExpatError as e:
                print(e, f)
                return None


def load_details(lines):
    text_lines = []
    if "Detalle" in lines:
        return lines["Detalle"]

    if lines:
        for line in lines:
            if "Detalle" in line:
                text_lines.append(line["Detalle"])
        return " | ".join(text_lines)

    return "-- no lines --"


def get_currency(data):
    if "CodigoTipoMoneda" in data["FacturaElectronica"]["ResumenFactura"].keys():
        return data["FacturaElectronica"]["ResumenFactura"]["CodigoTipoMoneda"]["CodigoMoneda"]
    return "CRC"


def get_exchange(data):
    if "CodigoTipoMoneda" in data["FacturaElectronica"]["ResumenFactura"].keys():
        return round(float(data["FacturaElectronica"]["ResumenFactura"]["CodigoTipoMoneda"]["TipoCambio"]), 2)
    return 0


def get_summary(data):
    summary = {
        "Fecha": data["FacturaElectronica"]["FechaEmision"].split("T")[0],
        "Factura": data["FacturaElectronica"]["NumeroConsecutivo"],
        "Proveedor": data["FacturaElectronica"]["Emisor"]["Nombre"],
        "Cliente": data["FacturaElectronica"]["Receptor"]["Nombre"],
        "Concepto": load_details(data["FacturaElectronica"]["DetalleServicio"]["LineaDetalle"]),
        "Moneda": get_currency(data),
        "Tipo de cambio": get_exchange(data),
        "Total Gravado": handle_empty("TotalGravado", data["FacturaElectronica"]["ResumenFactura"]),
        "Total Exento": handle_empty("TotalExento", data["FacturaElectronica"]["ResumenFactura"]),
        "Total Exonerado": handle_empty("TotalExonerado", data["FacturaElectronica"]["ResumenFactura"]),
        "Total Venta": handle_empty("TotalVenta", data["FacturaElectronica"]["ResumenFactura"]),
        "Total Descuentos": handle_empty("TotalDescuentos", data["FacturaElectronica"]["ResumenFactura"]),
        "Total Venta Neta": handle_empty("TotalVentaNeta", data["FacturaElectronica"]["ResumenFactura"]),
        "Total Impuesto": handle_empty("TotalImpuesto", data["FacturaElectronica"]["ResumenFactura"]),
        "Total Comprobante": handle_empty("TotalComprobante", data["FacturaElectronica"]["ResumenFactura"]),
        "Actividad del Proveedor": data["FacturaElectronica"]["CodigoActividad"],
        "email_provider": data['FacturaElectronica']["Emisor"]["CorreoElectronico"]
    }
    summary["invoice_type"] = "INGRESO" if summary["email_provider"] == REGISTER_EMAIL else "GASTO"
    summary["zip_name"] = f"{summary['Fecha']}.{data['FacturaElectronica']['Clave']}.zip"
    return summary


def create_temp_folder():
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)


def remove_temp_folder():
    if os.path.exists(TEMP_PATH):
        os.removedirs(TEMP_PATH)


def read_new_invoices():
    create_temp_folder()
    summarized = []

    clean_data()
    files = load_new_invoices()

    for zip_folder in files:
        unzip(zip_folder)
        data = find_xml()
        if data:
            summary = get_summary(data)
            summary["original_path"] = zip_folder
            summarized.append(summary)

        clean_data()

    remove_temp_folder()
    return summarized
