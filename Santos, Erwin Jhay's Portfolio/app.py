import math
from flask import Flask, render_template, request, redirect, url_for, flash
from linked_list import LinkedList
from stack import infix_to_postfix
from queues_deques import Queue

app = Flask(__name__)
app.secret_key = "change-me"

PROFILE = {
    "name": "Erwin Jhay Santos",
    "course": "BS Computer Engineering",
    "school": "Polytechnic University of the Philippines",
    "year": "2nd Year",
    "tagline": "Kapag nagbigay motibo, ilabas ang embutido.",
    "email": "santoserwimjhay105@gmail.com",
    "phone": "+63 969 403 4994",
    "location": "Marikina City, Metro Manila, Philippines",
    "github": "https://github.com/ej-snts",
}


@app.context_processor
def inject_profile():
    return {"p": PROFILE}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/works")
def works():
    return render_template("works.html")


@app.route("/touppercase", methods=["GET", "POST"])
def touppercase():
    text = result = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        result = text.upper()
    return render_template("touppercase.html", text=text, result=result)


def to_number(name):
    """Read a positive number from the form, or return None."""
    try:
        value = float(request.form.get(name, ""))
    except ValueError:
        return None
    return value if value > 0 else None


@app.route("/area-of-a-circle", methods=["GET", "POST"])
def circle():
    radius = area = error = None
    if request.method == "POST":
        radius = to_number("radius")
        if radius is None:
            error = "Enter a radius greater than 0."
        else:
            area = math.pi * radius ** 2
    return render_template("circle.html", radius=radius, area=area, error=error)


@app.route("/area-of-a-triangle", methods=["GET", "POST"])
def triangle():
    base = height = area = error = None
    if request.method == "POST":
        base, height = to_number("base"), to_number("height")
        if base is None or height is None:
            error = "Enter a base and a height greater than 0."
        else:
            area = 0.5 * base * height
    return render_template("triangle.html", base=base, height=height, area=area, error=error)


@app.route("/infix-to-postfix", methods=["GET", "POST"])
def postfix():
    expression = result = error = None
    steps = []
    if request.method == "POST":
        expression = request.form.get("expression", "").strip()
        try:
            result, steps = infix_to_postfix(expression)
        except ValueError as e:
            error = str(e)
    return render_template("postfix.html", expression=expression, result=result, steps=steps, error=error)


ll = LinkedList()
for _v in (10, 20, 30):
    ll.insert_at_end(_v)


def parse(text):
    """Turn form text into an int when possible, else keep it as a string."""
    text = text.strip()
    if text == "":
        return None
    try:
        return int(text)
    except ValueError:
        return text


def list_items():
    """Walk the list and collect each node's data for display."""
    items, node = [], ll.head
    while node:
        items.append(node.data)
        node = node.next
    return items


@app.route("/linked-list", methods=["GET", "POST"])
def linked_list():
    if request.method == "POST":
        action = request.form.get("action")
        value = parse(request.form.get("value", ""))
        target = parse(request.form.get("target", ""))

        needs_value = ("insert_beginning", "insert_end", "insert_after", "search", "remove_at")
        if action in needs_value and value is None:
            flash("Enter a value first.", "error")
        elif action == "insert_beginning":
            ll.insert_at_beginning(value)
            flash(f"Inserted {value} at the beginning.", "ok")
        elif action == "insert_end":
            ll.insert_at_end(value)
            flash(f"Inserted {value} at the end.", "ok")
        elif action == "insert_after":
            if target is None or not ll.search(target):
                flash(f"No node holds {target!r}, so nothing was inserted.", "error")
            else:
                ll.insert_after(target, value)
                flash(f"Inserted {value} after {target}.", "ok")
        elif action == "search":
            found = ll.search(value)
            flash(f"{value} was {'found' if found else 'not found'} in the list.", "ok" if found else "error")
        elif action == "remove_beginning":
            removed = ll.remove_beginning()
            if ll.head is None and removed is None:
                flash("The list is empty.", "error")
            else:
                flash(f"Removed {removed} from the beginning.", "ok")
        elif action == "remove_end":
            removed = ll.remove_at_end()
            if removed is None:
                flash("The list is empty.", "error")
            else:
                flash(f"Removed {removed} from the end.", "ok")
        elif action == "remove_at":
            removed = ll.remove_at(value)
            if removed is None:
                flash(f"No node holds {value}, so the list is unchanged.", "error")
            else:
                flash(f"Removed {removed} from the list.", "ok")
        elif action == "reset":
            ll.head = ll.tail = None
            flash("The list was cleared.", "ok")
        return redirect(url_for("linked_list"))   # avoids re-submitting on refresh
    return render_template("linked_list.html", items=list_items())


q = Queue()
for _v in (10, 20, 30):
    q.enqueue(_v)


@app.route("/queues-and-deques", methods=["GET", "POST"])
def queues_deques():
    if request.method == "POST":
        action = request.form.get("action")
        value = parse(request.form.get("value", ""))

        if action == "enqueue":
            if value is None:
                flash("Enter a value first.", "error")
            else:
                q.enqueue(value)
                flash(f"Enqueued {value} at the rear.", "ok")
        elif action == "dequeue":
            if q.is_empty():
                flash("The queue is empty.", "error")
            else:
                flash(f"Dequeued {q.dequeue()} from the front.", "ok")
        elif action == "peek":
            if q.is_empty():
                flash("The queue is empty.", "error")
            else:
                flash(f"The front of the queue is {q.peek()}.", "ok")
        elif action == "clear":
            q.clear()
            flash("The queue was cleared.", "ok")
        return redirect(url_for("queues_deques"))   # avoids re-submitting on refresh
    return render_template("queues_deques.html", items=q.items())


if __name__ == "__main__":
    app.run(debug=True)
