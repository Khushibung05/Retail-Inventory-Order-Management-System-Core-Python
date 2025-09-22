import argparse
import json
from src.services.product_service import ProductService
from src.services.customer_service import CustomerService
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService

# ---------------- SERVICES ----------------
product_service = ProductService()
customer_service = CustomerService()
order_service = OrderService()
payment_service = PaymentService()

# ---------------- PRODUCT COMMANDS ----------------
def cmd_product_add(args):
    try:
        p = product_service.add(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:", json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_list(args):
    try:
        products = product_service.list(limit=100)
        print(json.dumps(products, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_update(args):
    try:
        fields = {}
        if args.name: fields["name"] = args.name
        if args.sku: fields["sku"] = args.sku
        if args.price: fields["price"] = args.price
        if args.stock: fields["stock"] = args.stock
        if args.category: fields["category"] = args.category
        updated = product_service.update(args.id, **fields)
        print("Updated product:", json.dumps(updated, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_delete(args):
    try:
        deleted = product_service.delete(args.id)
        print("Deleted product:", json.dumps(deleted, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# ---------------- CUSTOMER COMMANDS ----------------
def cmd_customer_add(args):
    try:
        c = customer_service.add(args.name, args.email, args.phone, args.city)
        print("Created customer:", json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_list(args):
    try:
        customers = customer_service.list(limit=100)
        print(json.dumps(customers, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_update(args):
    try:
        fields = {}
        if args.phone: fields["phone"] = args.phone
        if args.city: fields["city"] = args.city
        updated = customer_service.update(args.id, **fields)
        print("Updated customer:", json.dumps(updated, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_delete(args):
    try:
        deleted = customer_service.delete(args.id)
        print("Deleted customer:", json.dumps(deleted, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_search(args):
    try:
        results = customer_service.search(email=args.email, city=args.city)
        print(json.dumps(results, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# ---------------- ORDER COMMANDS ----------------
def cmd_order_create(args):
    try:
        items = [{"prod_id": int(i.split(":")[0]), "quantity": int(i.split(":")[1])} for i in args.item]
        order = order_service.create_order(args.customer, items)
        print("Order created:", json.dumps(order, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_show(args):
    try:
        order = order_service.get_order_details(args.order)
        print(json.dumps(order, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_cancel(args):
    try:
        order_service.cancel_order(args.order)
        payment_service.refund_payment(args.order)
        print("Order cancelled and payment refunded")
    except Exception as e:
        print("Error:", e)

def cmd_order_complete(args):
    try:
        order_service.complete_order(args.order)
        print("Order completed")
    except Exception as e:
        print("Error:", e)

def cmd_order_list(args):
    try:
        orders = order_service.list_orders_by_customer(args.customer)
        print(json.dumps(orders, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# ---------------- PAYMENT COMMANDS ----------------
def cmd_payment_process(args):
    try:
        payment = payment_service.process_payment(args.order, args.method)
        print("Payment processed:", json.dumps(payment, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# ---------------- PARSER ----------------
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # Product commands
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")

    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)

    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)

    updatep = pprod_sub.add_parser("update")
    updatep.add_argument("--id", type=int, required=True)
    updatep.add_argument("--name")
    updatep.add_argument("--sku")
    updatep.add_argument("--price", type=float)
    updatep.add_argument("--stock", type=int)
    updatep.add_argument("--category")
    updatep.set_defaults(func=cmd_product_update)

    deletep = pprod_sub.add_parser("delete")
    deletep.add_argument("--id", type=int, required=True)
    deletep.set_defaults(func=cmd_product_delete)

    # Customer commands
    p_cust = sub.add_parser("customer", help="customer commands")
    pcust_sub = p_cust.add_subparsers(dest="action")

    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city")
    addc.set_defaults(func=cmd_customer_add)

    listc = pcust_sub.add_parser("list")
    listc.set_defaults(func=cmd_customer_list)

    updatec = pcust_sub.add_parser("update")
    updatec.add_argument("--id", type=int, required=True)
    updatec.add_argument("--phone")
    updatec.add_argument("--city")
    updatec.set_defaults(func=cmd_customer_update)

    deletec = pcust_sub.add_parser("delete")
    deletec.add_argument("--id", type=int, required=True)
    deletec.set_defaults(func=cmd_customer_delete)

    searchc = pcust_sub.add_parser("search")
    searchc.add_argument("--email")
    searchc.add_argument("--city")
    searchc.set_defaults(func=cmd_customer_search)

    # Order commands
    p_order = sub.add_parser("order", help="order commands")
    porder_sub = p_order.add_subparsers(dest="action")

    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", nargs="+", required=True, help="prod_id:qty")
    createo.set_defaults(func=cmd_order_create)

    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)

    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)

    completeo = porder_sub.add_parser("complete")
    completeo.add_argument("--order", type=int, required=True)
    completeo.set_defaults(func=cmd_order_complete)

    listo = porder_sub.add_parser("list")
    listo.add_argument("--customer", type=int, required=True)
    listo.set_defaults(func=cmd_order_list)

    # Payment commands
    p_payment = sub.add_parser("payment", help="payment commands")
    pay_sub = p_payment.add_subparsers(dest="action")

    process_pay = pay_sub.add_parser("process")
    process_pay.add_argument("--order", type=int, required=True)
    process_pay.add_argument("--method", choices=["Cash","Card","UPI"], required=True)
    process_pay.set_defaults(func=cmd_payment_process)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
