from utils import setup, read_new_invoices, read_new_pictures, generate_iva_summaries, move_invoices, move_pictures

if __name__ == '__main__':
    setup()
    invoices = read_new_invoices()
    pictures = read_new_pictures()
    incomes, expenses = generate_iva_summaries(invoices, pictures)
    move_invoices(invoices)
    move_pictures(pictures)
