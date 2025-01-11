import sqlite3 , uuid , qrcode , cv2

"Print Debug Messages If Set To True"
debug = True

def init_db():
    """
    This Function Should Be Run Once

    Initialize the SQLite database used to store ticket information.

    The database will have one table, 'tickets', with the following columns:

    - id: an auto-incrementing integer used as a primary key
    - uid: a TEXT field used to store the UID of the ticket
    - status: an INTEGER indicating the current status of the ticket (0 for unchecked, 1 for checked)
    """
    con = sqlite3.connect("tickets.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL UNIQUE,
            status INTEGER NOT NULL DEFAULT 0
        )
    """)

    con.commit()

def generate_ticket(prefix):

    uid = prefix + "-" + uuid.uuid4().hex

    con = sqlite3.connect("tickets.db")
    cur = con.cursor()

    cur.execute("""
        INSERT INTO tickets (uid) VALUES (?)
    """, (uid,))

    con.commit()

    qrcode.make(uid).save(uid + ".png")

    if debug: print("[*] Successfully created and saved ticket with UID:", uid)


def check_ticket(uid):
    """
    This function checks the status of the ticket with the given UID in the database.

    Args:
        uid (str): The UID of the ticket to be checked.

    Returns:
        int: 
            2 ticket has already been checked,
            1 ticket is successfully checked, 
            0 ticket does not exist.
    """

    con = sqlite3.connect("tickets.db")
    cur = con.cursor()

    cur.execute("SELECT status FROM tickets WHERE uid = ?", (uid,))

    ticket = cur.fetchone()

    if ticket is None:
        if debug: print("[*] Ticket with UID", uid, "does not exist")
        return 0
    
    if ticket[0] == 1:
        if debug: print("[*] Ticket with UID", uid, "has already been checked")
        return 2

    if ticket[0] == 0:
        cur.execute("""
            UPDATE tickets SET status = 1 WHERE uid = ?
        """, (uid,))
        if debug: print("[*] Ticket with UID", uid, "has been checked")

    con.commit()
    return 1


def get_all_tickets():
    con = sqlite3.connect("tickets.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM tickets")

    for row in cur.fetchall():
        print(row)

def delete_all_tickets():
    con = sqlite3.connect("tickets.db")
    cur = con.cursor()

    cur.execute("DELETE FROM tickets")
    con.commit()

    if debug: print("[*] Successfully deleted all tickets")

def delete_ticket_by_id(id):
    con = sqlite3.connect("tickets.db")
    cur = con.cursor()

    cur.execute("DELETE FROM tickets WHERE id = ?", (id,))
    con.commit()

    if debug: print("[*] Successfully deleted ticket with ID:", id)

def delete_ticket_by_uid(uid):
    con = sqlite3.connect("tickets.db")
    cur = con.cursor()

    cur.execute("DELETE FROM tickets WHERE uid = ?", (uid,))
    con.commit()
    
    if debug: print("[*] Successfully deleted ticket with UID:", uid)

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    qr_detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Detect and decode the QR code in the frame
        decoded_text, pts, qr_code = qr_detector.detectAndDecode(frame)

        if decoded_text:

            ticket = check_ticket(decoded_text)

            if(ticket == 1):
                # Draw a green rectangle around the QR code
                frame[:] = (0, 255, 0)    

                font = cv2.FONT_HERSHEY_SIMPLEX
                text = "Success"
                text_size = cv2.getTextSize(text, font, 1, 2)[0]

                # Get the position to center the text
                text_x = (frame.shape[1] - text_size[0]) // 2
                text_y = (frame.shape[0] + text_size[1]) // 2

                cv2.putText(frame, text, (text_x, text_y), font, 1, (0, 0, 0), 2)

                # Display the frame and wait for 2.5 seconds before scanning the next QR code
                cv2.imshow('Ticket Scanner | Lukkshh', frame)
                cv2.waitKey(2500)

            elif(ticket == 2):
                frame[:] = (255, 0, 0)    

                font = cv2.FONT_HERSHEY_SIMPLEX
                text = "Already Checked"
                text_size = cv2.getTextSize(text, font, 1, 2)[0]

                # Get the position to center the text
                text_x = (frame.shape[1] - text_size[0]) // 2
                text_y = (frame.shape[0] + text_size[1]) // 2

                cv2.putText(frame, text, (text_x, text_y), font, 1, (0, 0, 0), 2)
            
                # Display the frame and wait for 2.5 seconds before scanning the next QR code
                cv2.imshow('Ticket Scanner | Lukkshh', frame)
                cv2.waitKey(2500)
            
            elif(ticket == 0):

                frame[:] = (0, 0, 255)    

                font = cv2.FONT_HERSHEY_SIMPLEX
                text = "Ticket Doesn't Exist"
                text_size = cv2.getTextSize(text, font, 1, 2)[0]

                # Get the position to center the text
                text_x = (frame.shape[1] - text_size[0]) // 2
                text_y = (frame.shape[0] + text_size[1]) // 2

                cv2.putText(frame, text, (text_x, text_y), font, 1, (0, 0, 0), 2)

                # Display the frame and wait for 2.5 seconds before scanning the next QR code
                cv2.imshow('Ticket Scanner | Lukkshh', frame)
                cv2.waitKey(2500)

        cv2.imshow('Ticket Scanner | Lukkshh', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def help():
    print("1. Initialize Database \t 6. Help")
    print("2. Generate Ticket \t 7. Delete All Tickets ")
    print("3. Check Ticket \t 8. Delete Ticket by ID")
    print("4. Get All Ticket \t 9. Delete Ticket by UID")
    print("5. Open Scanner \t 0. Exit")
    

def main():
    help()

    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            init_db()
        elif choice == "2":
            prefix = input("Enter the prefix for the ticket: ")
            generate_ticket(prefix)
        elif choice == "3":
            uid = input("Enter the UID of the ticket: ")
            check_ticket(uid)
        elif choice == "4":
            get_all_tickets()
        elif choice == "5":
            scan_qr_code()
        elif choice == "6":
            help()
        elif choice == "7":
            delete_all_tickets()
        elif choice == "8":
            id = input("Enter the ID of the ticket: ")
            delete_ticket_by_id(id)
        elif choice == "9":
            uid = input("Enter the UID of the ticket: ")
            delete_ticket_by_uid(uid)
        elif choice == "0":
            break

if __name__ == "__main__":
    main()