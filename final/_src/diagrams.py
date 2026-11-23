# UML diagram specs.  Colours: w=normal class, b=superclass/abstract, t=subclass, o=highlight, y=external/db
D = {}

# ---------- index: mock paper Q24 (cinema) ----------
D["mock-cinema"] = {"type": "class", "w": 760, "h": 560, "alt": "cinema booking class diagram", "classes": {
    "Cinema":   {"x": 10,  "y": 10,  "attrs": ["name", "address"], "ops": ["addHall()"]},
    "Hall":     {"x": 10,  "y": 175, "attrs": ["hallNo"], "ops": ["getSeats()"]},
    "Seat":     {"x": 10,  "y": 340, "attrs": ["row", "number"], "ops": ["isFree(screening)"]},
    "Movie":    {"x": 560, "y": 10,  "attrs": ["title", "duration"], "ops": ["getInfo()"]},
    "Screening": {"x": 290, "y": 175, "attrs": ["startTime"], "ops": ["getAvailableSeats()"]},
    "Booking":  {"x": 290, "y": 340, "attrs": ["bookingNo"], "ops": ["calculateTotal()"]},
    "Customer": {"x": 560, "y": 300, "attrs": ["name"], "ops": ["makeBooking()", "cancelBooking()"], "c": "b", "abstract": True},
    "Member":   {"x": 470, "y": 455, "attrs": ["memberID", "points"], "ops": ["redeemPoints()"], "c": "t"},
    "Guest":    {"x": 650, "y": 455, "attrs": ["email"], "ops": ["register()"], "c": "t"},
}, "links": [
    {"a": "Hall", "b": "Cinema", "kind": "comp", "ma": "1..*", "mb": "1"},
    {"a": "Seat", "b": "Hall", "kind": "comp", "ma": "1..*", "mb": "1"},
    {"a": "Screening", "b": "Hall", "ma": "*", "mb": "1"},
    {"a": "Screening", "b": "Movie", "ma": "*", "mb": "1"},
    {"a": "Booking", "b": "Screening", "ma": "*", "mb": "1"},
    {"a": "Booking", "b": "Seat", "ma": "*", "mb": "1..*"},
    {"a": "Booking", "b": "Customer", "ma": "*", "mb": "1"},
    {"a": "Member", "b": "Customer", "kind": "gen"},
    {"a": "Guest", "b": "Customer", "kind": "gen"},
]}

# ---------- index: mock paper Q25 (ATM withdrawal) ----------
D["mock-atm"] = {"type": "seq", "dx": 165, "x0": 60, "padr": 120, "alt": "ATM withdrawal sequence diagram", "minw": 640,
 "parts": [{"n": "Customer", "actor": True}, {"n": ":ATM"}, {"n": ":BankServer"}, {"n": ":AccountDB", "db": True}],
 "msgs": [
    {"f": 0, "t": 1, "l": "insertCard()"},
    {"f": 0, "t": 1, "l": "enterPIN(pin)"},
    {"f": 1, "t": 2, "l": "verify(cardNo, pin)"},
    {"f": 2, "t": 3, "l": "getAccount(cardNo)"},
    {"f": 3, "t": 2, "l": "account", "r": True},
    {"f": 2, "t": 1, "l": "valid / invalid", "r": True},
    {"f": 0, "t": 1, "l": "enterAmount(amt)", "gap": 14},
    {"f": 1, "t": 2, "l": "withdraw(cardNo, amt)"},
    {"f": 2, "t": 3, "l": "getBalance(cardNo)"},
    {"f": 3, "t": 2, "l": "balance", "r": True},
    {"f": 2, "t": 3, "l": "updateBalance(cardNo, -amt)", "gap": 14},
    {"f": 2, "t": 1, "l": "success", "r": True},
    {"f": 1, "t": 1, "l": "dispenseCash(amt)"},
    {"f": 1, "t": 0, "l": "cash, receipt", "r": True},
    {"f": 2, "t": 1, "l": "insufficientFunds", "r": True, "gap": 6},
    {"f": 1, "t": 0, "l": "showError(\"insufficient\")"},
    {"f": 1, "t": 0, "l": "showError(\"invalid PIN\")", "gap": 6},
    {"f": 1, "t": 0, "l": "ejectCard()", "gap": 14},
 ],
 "frames": [
    {"k": "alt", "g": "[PIN valid]", "from": 6, "to": 16, "p0": 0, "p1": 3, "padl": 45, "padr": 95, "else": [(16, "[else]")]},
    {"k": "alt", "g": "[balance >= amt]", "from": 10, "to": 15, "p0": 0, "p1": 3, "padl": 30, "padr": 80, "else": [(14, "[else]")]},
 ]}

# ================= P1 UML =================
D["p1-octopus"] = {"type": "class", "w": 300, "h": 130, "alt": "class box anatomy", "classes": {
    "Octopus": {"x": 60, "y": 10, "attrs": ["- amount: float", "- ID: String"], "ops": ["+ getAmount(): float", "+ getID(): String", "+ withdraw(x: int)"], "c": "o"}}}

def _pair(rows, w=370):
    cls, links = {}, []
    for i, (a, b, kind, la, lb, lab) in enumerate(rows):
        y = 10 + i * 64
        cls[a] = {"x": 8, "y": y, "compact": True}
        cls[b] = {"x": w - 8 - (len(b) * 7.75 + 18), "y": y, "compact": True}
        links.append({"a": a, "b": b, "kind": kind, "ma": la, "mb": lb, "label": lab, "ldy": -8})
    return cls, links

_c, _l = _pair([("Game", "Clock", "dep", "", "", "dependency（用到）"),
                ("Person", "Company", "assoc", "*", "*", "association"),
                ("Course", "Curriculum", "agg", "*", "*", "aggregation ◇"),
                ("Room", "Building", "comp", "1..*", "1", "composition ◆"),
                ("Student", "Person ", "gen", "", "", "generalization △"),
                ("ArrayList", "List", "real", "", "", "realization（implements）")])
_c["List"]["stereo"] = "interface"; _c["List"]["y"] -= 7; _c["List"]["x"] -= 30; _c["List"]["c"] = "b"; _c["Person "]["c"] = "b"; _c["Person "]["label"] = "Person"
D["p1-rels"] = {"type": "class", "w": 370, "h": 390, "alt": "six relationship notations", "classes": _c, "links": _l}

_c, _l = _pair([("City", "Country", "assoc", "1", "0..1", "is capital of"),
                ("Child", "Mother", "assoc", "1..*", "1", "has"),
                ("Person", "Company", "assoc", "*", "*", "works for")])
D["p1-mult"] = {"type": "class", "w": 370, "h": 200, "alt": "multiplicity examples", "classes": _c, "links": _l}

D["p1-l5-order"] = {"type": "class", "w": 600, "h": 300, "alt": "lecture example class diagram", "classes": {
    "Customer": {"x": 10, "y": 10, "attrs": ["- customerId: String", "- name: String", "- email: String"], "ops": ["+ createOrder()"]},
    "Order": {"x": 330, "y": 10, "attrs": ["- orderId: String", "- orderDate: Date", "- status: String"], "ops": ["+ calculateTotal(): Double"]},
    "OrderItem": {"x": 330, "y": 175, "attrs": ["- quantity: int", "- priceAtPurchase: Double"], "ops": ["+ getSubtotal(): Double"]},
    "Product": {"x": 10, "y": 165, "attrs": ["- productId: String", "- name: String", "- unitPrice: Double", "- stockQuantity: int"], "ops": ["+ updateStock(qty: int)"]},
}, "links": [
    {"a": "Customer", "b": "Order", "ma": "1", "mb": "0..*", "label": "places"},
    {"a": "Order", "b": "OrderItem", "ma": "1", "mb": "1..*", "label": "contains", "ldx": 34, "ldy": 0},
    {"a": "OrderItem", "b": "Product", "ma": "*", "mb": "1", "label": "references"},
]}

D["p1-domain-lib"] = {"type": "class", "w": 560, "h": 330, "alt": "library domain model", "classes": {
    "Member": {"x": 10, "y": 10, "attrs": ["id", "name"], "ops": [], "minw": 110},
    "Loan": {"x": 230, "y": 10, "attrs": ["dueDate"], "ops": [], "minw": 100},
    "Catalog": {"x": 450, "y": 10, "attrs": [], "ops": [], "minw": 100},
    "LibraryItem": {"x": 210, "y": 140, "attrs": ["id", "title"], "ops": [], "c": "b"},
    "Book": {"x": 70, "y": 260, "attrs": ["21 days; max 6"], "ops": [], "c": "t", "compact": True},
    "CD": {"x": 245, "y": 260, "attrs": [], "ops": [], "c": "t", "compact": True, "minw": 70},
    "Magazine": {"x": 380, "y": 260, "attrs": [], "ops": [], "c": "t", "compact": True},
}, "links": [
    {"a": "Member", "b": "Loan", "ma": "1", "mb": "0..*", "label": "borrows"},
    {"a": "Loan", "b": "LibraryItem", "ma": "0..*", "mb": "1", "label": "records", "ldx": 34, "ldy": 0},
    {"a": "Catalog", "b": "LibraryItem", "ma": "1", "mb": "0..*", "label": "stocks"},
    {"a": "Book", "b": "LibraryItem", "kind": "gen"},
    {"a": "CD", "b": "LibraryItem", "kind": "gen"},
    {"a": "Magazine", "b": "LibraryItem", "kind": "gen"},
]}

# 2025 Q24 library
D["p1-2025-lib"] = {"type": "class", "w": 700, "h": 420, "alt": "2025 Q24 library class diagram", "classes": {
    "Category": {"x": 10, "y": 10, "attrs": ["name"], "ops": ["addItem(item)", "searchItems(keyword)"]},
    "LibraryItem": {"x": 300, "y": 10, "attrs": ["id", "title", "isAvailable"], "ops": ["checkIn()", "checkOut()"], "c": "b", "abstract": True},
    "Book": {"x": 200, "y": 210, "attrs": ["isbn", "authors[1..*]"], "ops": ["getAuthors()"], "c": "t"},
    "DVD": {"x": 380, "y": 210, "attrs": ["director", "runtimeSeconds"], "ops": ["getRuntime()"], "c": "t"},
    "Loan": {"x": 590, "y": 10, "attrs": ["loanID", "dueDate"], "ops": ["calculateFine()"]},
    "User": {"x": 590, "y": 230, "attrs": ["id", "name"], "ops": ["borrowItem(item)", "returnItem(item)"]},
}, "links": [
    {"a": "LibraryItem", "b": "Category", "kind": "agg", "ma": "0..*", "mb": "1"},
    {"a": "Loan", "b": "LibraryItem", "ma": "0..*", "mb": "1..*", "label": "covers"},
    {"a": "Loan", "b": "User", "ma": "0..*", "mb": "1", "label": "borrows", "ldx": 32, "ldy": 0},
    {"a": "Book", "b": "LibraryItem", "kind": "gen"},
    {"a": "DVD", "b": "LibraryItem", "kind": "gen"},
]}

# 2022 Q24 / Asm2 Q1 order management
D["p1-2022-order"] = {"type": "class", "w": 640, "h": 450, "alt": "2022 Q24 order management class diagram", "classes": {
    "Customer": {"x": 10, "y": 10, "attrs": ["phoneNumber", "address"], "ops": ["placeOrder()"], "c": "b", "abstract": True},
    "Person": {"x": 10, "y": 190, "attrs": ["firstName", "lastName"], "ops": ["getName()"], "c": "t"},
    "Company": {"x": 150, "y": 190, "attrs": ["registrationNumber"], "ops": ["getRegNo()"], "c": "t"},
    "Order": {"x": 360, "y": 10, "attrs": ["date"], "ops": ["addItem(item)", "getTotal()"]},
    "OrderItem": {"x": 360, "y": 190, "attrs": ["quantity", "price"], "ops": ["OrderItem(order, product, qty)"]},
    "Product": {"x": 360, "y": 345, "attrs": ["name", "price", "quantityInStock"], "ops": ["updatePrice()", "updateQuantity()"]},
}, "links": [
    {"a": "Customer", "b": "Order", "ma": "1", "mb": "0..*", "label": "places"},
    {"a": "OrderItem", "b": "Order", "kind": "comp", "ma": "1..*", "mb": "1"},
    {"a": "OrderItem", "b": "Product", "ma": "0..*", "mb": "1", "label": "for", "ldx": 22, "ldy": 0},
    {"a": "Person", "b": "Customer", "kind": "gen"},
    {"a": "Company", "b": "Customer", "kind": "gen"},
]}

# 2023 Q24 banking
D["p1-2023-bank"] = {"type": "class", "w": 880, "h": 450, "alt": "2023 Q24 banking class diagram", "classes": {
    "DebitCard": {"x": 10, "y": 10, "attrs": ["cardNumber"], "ops": ["accessAccounts()"]},
    "Customer": {"x": 10, "y": 200, "attrs": ["id", "name", "mailingAddress"], "ops": ["openAccount()"]},
    "Account": {"x": 300, "y": 110, "attrs": ["accountID", "balance"], "ops": ["deposit(amount)", "withdraw(amount)", "checkBalance()"], "c": "b", "abstract": True},
    "SavingsAccount": {"x": 170, "y": 340, "attrs": ["interestRate"], "ops": ["addInterest()"], "c": "t"},
    "CurrencyAccount": {"x": 340, "y": 340, "attrs": ["currency"], "ops": ["convert()"], "c": "t"},
    "Transaction": {"x": 640, "y": 110, "attrs": ["dateTime", "amount"], "ops": ["record()"], "c": "b", "abstract": True},
    "Deposit": {"x": 545, "y": 300, "attrs": [], "ops": [], "c": "t", "compact": True},
    "Withdrawal": {"x": 650, "y": 300, "attrs": [], "ops": [], "c": "t", "compact": True},
    "BalanceCheck": {"x": 770, "y": 300, "attrs": [], "ops": [], "c": "t", "compact": True},
}, "links": [
    {"a": "Customer", "b": "DebitCard", "ma": "1", "mb": "1", "label": "owns", "ldx": 24, "ldy": 0},
    {"a": "Customer", "b": "Account", "ma": "1..2", "mb": "1..*", "label": "owns"},
    {"a": "DebitCard", "b": "Account", "ma": "1..2", "mb": "1..*", "label": "accesses"},
    {"a": "Transaction", "b": "Account", "kind": "comp", "ma": "0..*", "mb": "1", "label": "records"},
    {"a": "SavingsAccount", "b": "Account", "kind": "gen"},
    {"a": "CurrencyAccount", "b": "Account", "kind": "gen"},
    {"a": "Deposit", "b": "Transaction", "kind": "gen"},
    {"a": "Withdrawal", "b": "Transaction", "kind": "gen"},
    {"a": "BalanceCheck", "b": "Transaction", "kind": "gen"},
]}

# 2024 Q24 hospital
D["p1-2024-hosp"] = {"type": "class", "w": 860, "h": 540, "alt": "2024 Q24 hospital class diagram", "classes": {
    "Hospital": {"x": 10, "y": 10, "attrs": ["name", "address", "phoneNumber"], "ops": ["addDepartment()"]},
    "Department": {"x": 10, "y": 220, "attrs": ["name"], "ops": ["addStaff()", "removeStaff()"]},
    "Person": {"x": 360, "y": 10, "attrs": ["name", "birthDate", "gender", "homeAddress", "phoneNumber"], "ops": ["updateContact()"], "c": "b", "abstract": True},
    "Staff": {"x": 240, "y": 250, "attrs": ["certifications[*]", "languages[*]"], "ops": ["addCertification()"], "c": "b", "abstract": True},
    "Patient": {"x": 640, "y": 250, "attrs": ["patientID", "allergies[*]"], "ops": ["addAllergy()"], "c": "t"},
    "Nurse": {"x": 130, "y": 450, "attrs": [], "ops": [], "c": "t", "compact": True},
    "TechnicalStaff": {"x": 200, "y": 450, "attrs": [], "ops": [], "c": "t", "compact": True},
    "AdminStaff": {"x": 340, "y": 450, "attrs": [], "ops": [], "c": "t", "compact": True},
    "Doctor": {"x": 450, "y": 430, "attrs": [], "ops": ["writePrescription()"], "c": "t"},
    "Prescription": {"x": 740, "y": 420, "attrs": ["prescriptionID", "sickness", "medication"], "ops": ["print()"]},
}, "links": [
    {"a": "Department", "b": "Hospital", "kind": "comp", "ma": "1..*", "mb": "1"},
    {"a": "Staff", "b": "Department", "kind": "agg", "ma": "1..*", "mb": "1"},
    {"a": "Staff", "b": "Person", "kind": "gen"},
    {"a": "Patient", "b": "Person", "kind": "gen"},
    {"a": "Doctor", "b": "Staff", "kind": "gen"},
    {"a": "Nurse", "b": "Staff", "kind": "gen"},
    {"a": "TechnicalStaff", "b": "Staff", "kind": "gen"},
    {"a": "AdminStaff", "b": "Staff", "kind": "gen"},
    {"a": "Prescription", "b": "Doctor", "ma": "0..*", "mb": "1", "label": "writes"},
    {"a": "Prescription", "b": "Patient", "ma": "0..*", "mb": "1", "label": "for", "ldx": 18, "ldy": 0},
]}

# ---- sequence diagrams ----
D["p1-seq-patient"] = {"type": "seq", "dx": 150, "x0": 60, "padr": 90, "alt": "view patient info sequence", "minw": 560,
 "parts": [{"n": "Receptionist", "actor": True}, {"n": "P:PatientInfo"}, {"n": "D:PatientDB", "db": True}, {"n": "AS:Authorization"}],
 "msgs": [
    {"f": 0, "t": 1, "l": "ViewInfo(PID)"},
    {"f": 1, "t": 2, "l": "report(Info, PID, UID)"},
    {"f": 2, "t": 3, "l": "authorize(Info, UID)"},
    {"f": 3, "t": 2, "l": "authorization", "r": True},
    {"f": 2, "t": 1, "l": "Patient info", "r": True},
    {"f": 2, "t": 1, "l": "Error(no access)", "r": True},
 ],
 "act": [(1, 0, 5), (2, 1, 5)],
 "frames": [{"k": "alt", "g": "[authorization OK]", "from": 4, "to": 5, "p0": 0, "p1": 2, "padl": 30, "padr": 90, "else": [(5, "[authorization fail]")]}]}

D["p1-seq-frames"] = {"type": "seq", "dx": 170, "x0": 60, "padr": 80, "alt": "loop and opt frames", "minw": 420,
 "parts": [{"n": "Cashier", "actor": True}, {"n": ":Register"}, {"n": ":Sale"}],
 "msgs": [
    {"f": 0, "t": 1, "l": "makeNewSale()"},
    {"f": 1, "t": 2, "l": "create()", "create": True},
    {"f": 0, "t": 1, "l": "enterItem(id, qty)"},
    {"f": 1, "t": 2, "l": "addLine(id, qty)"},
    {"f": 1, "t": 0, "l": "description, total", "r": True},
    {"f": 0, "t": 1, "l": "applyCoupon(code)"},
    {"f": 1, "t": 2, "l": "discount(code)"},
    {"f": 0, "t": 1, "l": "endSale()"},
 ],
 "frames": [{"k": "loop", "g": "[more items]", "from": 2, "to": 4, "p0": 0, "p1": 2, "padl": 40, "padr": 60},
            {"k": "opt", "g": "[has coupon]", "from": 5, "to": 6, "p0": 0, "p1": 2, "padl": 40, "padr": 60}]}

D["p1-2022-flight"] = {"type": "seq", "dx": 165, "x0": 60, "padr": 110, "alt": "2022 Q25 flight booking sequence", "minw": 760,
 "parts": [{"n": "Customer", "actor": True}, {"n": ":BookingSystem"}, {"n": ":FlightDB", "db": True}, {"n": ":CustomerDB", "db": True}, {"n": ":ReservationSystem", "db": True}],
 "msgs": [
    {"f": 0, "t": 1, "l": "searchFlights(criteria)"},
    {"f": 1, "t": 2, "l": "queryFlights(criteria)"},
    {"f": 2, "t": 1, "l": "matchingFlights", "r": True},
    {"f": 1, "t": 0, "l": "flightList", "r": True},
    {"f": 0, "t": 1, "l": "viewBundle(bundleID)"},
    {"f": 1, "t": 0, "l": "bundleDetails", "r": True},
    {"f": 0, "t": 1, "l": "book(bundleID)"},
    {"f": 1, "t": 0, "l": "requestCredentials()"},
    {"f": 0, "t": 1, "l": "login(user, password)"},
    {"f": 1, "t": 3, "l": "validate(user, password)"},
    {"f": 3, "t": 1, "l": "valid", "r": True},
    {"f": 1, "t": 0, "l": "loggedIn", "r": True},
    {"f": 0, "t": 1, "l": "enterPassengers(info)"},
    {"f": 0, "t": 1, "l": "selectSeats(seats)"},
    {"f": 0, "t": 1, "l": "confirmAndPay(payment)"},
    {"f": 1, "t": 3, "l": "storePassengers(info)"},
    {"f": 1, "t": 4, "l": "makeBooking(bundle, info, seats)"},
    {"f": 4, "t": 1, "l": "bookingRef", "r": True},
    {"f": 1, "t": 0, "l": "sendConfirmation(bookingRef)"},
 ]}

D["p1-2025-checkout"] = {"type": "seq", "dx": 150, "x0": 50, "padr": 90, "alt": "2025 Q25 library checkout sequence", "minw": 980,
 "parts": [{"n": "User", "actor": True}, {"n": "Librarian", "actor": True}, {"n": ":LMS"}, {"n": ":UserDB", "db": True}, {"n": ":BookDB", "db": True}, {"n": ":LoanDB", "db": True}, {"n": ":LoanRecord"}],
 "msgs": [
    {"f": 0, "t": 1, "l": "userID, books"},
    {"f": 1, "t": 2, "l": "verifyUser(userID)"},
    {"f": 2, "t": 3, "l": "getUser(userID)"},
    {"f": 3, "t": 2, "l": "userInfo", "r": True},
    {"f": 2, "t": 6, "l": "«create» LoanRecord(userID, dueDate)", "create": True},
    {"f": 2, "t": 1, "l": "eligible", "r": True},
    {"f": 1, "t": 2, "l": "processBook(bookID)"},
    {"f": 2, "t": 4, "l": "isAvailable(bookID)"},
    {"f": 4, "t": 2, "l": "available", "r": True},
    {"f": 2, "t": 6, "l": "addBook(bookID)"},
    {"f": 2, "t": 4, "l": "setStatus(bookID, unavailable)"},
    {"f": 2, "t": 5, "l": "store(loanRecord)"},
    {"f": 2, "t": 1, "l": "dueDate, loanID", "r": True},
    {"f": 1, "t": 0, "l": "dueDate, loanID", "r": True},
    {"f": 2, "t": 1, "l": "notEligible", "r": True},
 ],
 "frames": [
    {"k": "alt", "g": "[user found and quota > 0]", "from": 4, "to": 14, "p0": 1, "p1": 6, "padl": 40, "padr": 70, "else": [(14, "[else]")]},
    {"k": "loop", "g": "[for each requested book]", "from": 6, "to": 10, "p0": 1, "p1": 6, "padl": 28, "padr": 58, "bpad": 8},
    {"k": "opt", "g": "[available]", "from": 9, "to": 10, "p0": 2, "p1": 6, "padl": 20, "padr": 46},
 ]}

D["p1-l5-food"] = {"type": "seq", "dx": 165, "x0": 60, "padr": 100, "alt": "L5 exercise food order sequence", "minw": 820,
 "parts": [{"n": "Customer", "actor": True}, {"n": ":FoodDeliveryApp"}, {"n": ":RestaurantService"}, {"n": ":PaymentGateway"}, {"n": ":NotificationService"}, {"n": ":Order"}],
 "msgs": [
    {"f": 0, "t": 1, "l": "submitOrder(items, address)"},
    {"f": 1, "t": 2, "l": "checkOrder(items)"},
    {"f": 2, "t": 1, "l": "confirmation, totalPrice", "r": True},
    {"f": 1, "t": 3, "l": "requestPayment(totalPrice)"},
    {"f": 3, "t": 1, "l": "success / failure", "r": True},
    {"f": 1, "t": 4, "l": "notifyOrderConfirmed(customerEmail)"},
    {"f": 1, "t": 2, "l": "prepareOrder(orderDetails)"},
    {"f": 2, "t": 5, "l": "«create»", "create": True},
    {"f": 1, "t": 0, "l": "orderConfirmed(orderId, eta)"},
    {"f": 1, "t": 0, "l": "orderFailed(\"Payment declined\")"},
 ],
 "frames": [{"k": "alt", "g": "[payment successful]", "from": 5, "to": 9, "p0": 0, "p1": 5, "padl": 40, "padr": 60, "else": [(9, "[else]")]}]}

# ================= P7 Design/OO =================
D["p7-poly"] = {"type": "class", "w": 380, "h": 300, "alt": "LibraryItem polymorphism", "minw": 0, "classes": {
    "LibraryItem": {"x": 75, "y": 5, "attrs": ["- itemId", "- title", "- loan"], "ops": ["+ loanDays(): int", "+ borrowLimit(): int", "+ checkout(member, today)"], "c": "b", "abstract": True},
    "Book": {"x": 5, "y": 200, "attrs": [], "ops": ["loanDays() → 21", "borrowLimit() → 6"], "c": "t"},
    "CD": {"x": 192, "y": 200, "attrs": [], "ops": ["loanDays() → 7"], "c": "t"},
    "Magazine": {"x": 300, "y": 160, "attrs": [], "ops": [], "c": "t", "compact": True},
}, "links": [
    {"a": "Book", "b": "LibraryItem", "kind": "gen"},
    {"a": "CD", "b": "LibraryItem", "kind": "gen"},
    {"a": "Magazine", "b": "LibraryItem", "kind": "gen"},
]}
D["p7-ocp"] = {"type": "class", "w": 380, "h": 250, "alt": "open closed principle", "minw": 0, "classes": {
    "Progress": {"x": 5, "y": 10, "attrs": ["- m: Measurable"], "ops": ["+ getAsPercent()"], "c": "o"},
    "Measurable": {"x": 205, "y": 5, "attrs": [], "ops": ["getTotal()", "getPartial()"], "c": "b", "stereo": "interface"},
    "File": {"x": 160, "y": 175, "attrs": [], "ops": [], "c": "t", "compact": True},
    "Computation": {"x": 255, "y": 175, "attrs": [], "ops": [], "c": "t", "compact": True},
}, "links": [
    {"a": "Progress", "b": "Measurable", "nav": True, "ma": "", "mb": "1"},
    {"a": "File", "b": "Measurable", "kind": "real"},
    {"a": "Computation", "b": "Measurable", "kind": "real"},
]}
D["p7-dip"] = {"type": "class", "w": 380, "h": 240, "alt": "dependency inversion", "minw": 0, "classes": {
    "EBookReader": {"x": 5, "y": 10, "attrs": ["- ebook: EBook"], "ops": ["+ read()"], "c": "o"},
    "EBook": {"x": 230, "y": 5, "attrs": [], "ops": ["read()"], "c": "b", "stereo": "interface"},
    "PDFBook": {"x": 165, "y": 170, "attrs": [], "ops": [], "c": "t", "compact": True},
    "MobiBook": {"x": 270, "y": 170, "attrs": [], "ops": [], "c": "t", "compact": True},
}, "links": [
    {"a": "EBookReader", "b": "EBook", "nav": True, "mb": "1"},
    {"a": "PDFBook", "b": "EBook", "kind": "real"},
    {"a": "MobiBook", "b": "EBook", "kind": "real"},
]}
D["p7-composite"] = {"type": "class", "w": 380, "h": 230, "alt": "composite pattern", "minw": 0, "classes": {
    "Component": {"x": 110, "y": 5, "attrs": [], "ops": ["operation()"], "c": "b", "abstract": True},
    "Leaf": {"x": 20, "y": 150, "attrs": [], "ops": ["operation()"], "c": "t"},
    "Composite": {"x": 200, "y": 150, "attrs": ["- children"], "ops": ["operation()", "add(c)"], "c": "t"},
}, "links": [
    {"a": "Leaf", "b": "Component", "kind": "gen"},
    {"a": "Composite", "b": "Component", "kind": "gen", "ax": 0.35, "ay": 0.0, "bx": 0.6, "by": 1.0},
    {"a": "Component", "b": "Composite", "kind": "agg", "ma": "0..*", "mb": "1", "ax": 1.0, "ay": 0.3, "bx": 0.95, "by": 0.0, "via": [(298, 26)], "off": -1},
]}
