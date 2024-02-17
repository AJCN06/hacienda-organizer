import pandas as pd
import os
from .settings import SUMMARIES_PATH, handle_empty
from datetime import date


def export_data(name, data):
    dfs = pd.DataFrame(data)
    dfs.to_excel(os.path.join(SUMMARIES_PATH, f"{date.today()} - {name}.xlsx"), index=True, header=True)


def normalize_invoice(invoice):
    return {
        "Fecha": handle_empty("Fecha", invoice),
        "Factura": handle_empty("Factura", invoice),
        "Referencia Comprobante": handle_empty("Referencia", invoice),
        "Proveedor": handle_empty("Proveedor", invoice),
        "Concepto": handle_empty("Concepto", invoice),
        "Moneda": handle_empty("Moneda", invoice),
        "Total Gravado": handle_empty("Total Gravado", invoice),
        "Total Exento": handle_empty("Total Exonerado", invoice),
        "No sujeto": handle_empty("Total Exento", invoice),
        "Bouchers": handle_empty("Bouchers", invoice),
        "IVA": handle_empty("Total Impuesto", invoice),
        "Total": handle_empty("Total Comprobante", invoice),
        "T.C.V": max(handle_empty("Tipo de cambio", invoice), 1) if handle_empty("Tipo de cambio", invoice) else 1,
        "Cliente": handle_empty("Cliente", invoice) if not invoice["invoice_type"] == "GASTO" else ""
    }


def normalize_picture(picture):
    return {
        "Fecha": handle_empty("Fecha", picture),
        "Factura": handle_empty("Factura", picture),
        "Referencia Comprobante": handle_empty("Referencia", picture),
        "Proveedor": handle_empty("Comercio", picture),
        "Concepto": handle_empty("Tipo de Transaccion", picture),
        "Moneda": handle_empty("Monto", picture).split(" ")[-2],
        "Total Gravado": handle_empty("Total Gravado", picture),
        "Total Exento": handle_empty("Total Exento", picture),
        "No sujeto": handle_empty("No sujeto", picture),
        "Bouchers": handle_empty("Monto", picture).split(" ")[-1],
        "IVA": handle_empty("IVA", picture),
        "Total": handle_empty("Monto", picture).split(" ")[-1],
        "T.C.V": handle_empty("T.C.V", picture),
        "Cliente": handle_empty("Cliente", picture)
    }


def generate_iva_summaries(invoices, pictures):
    incomes, expenses = [], []

    for invoice in invoices:
        if invoice["invoice_type"] == "GASTO":
            expenses.append(normalize_invoice(invoice))
        else:
            incomes.append(normalize_invoice(invoice))
    for pic in pictures:
        expenses.append(normalize_picture(pic))

    export_data("invoices", invoices)
    export_data("pictures", pictures)
    export_data("incomes", incomes)
    export_data("expenses", expenses)

    return incomes, expenses
