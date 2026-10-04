from flask import Flask, render_template, request, redirect, url_for, session
from compiler.grammar import Grammar

app = Flask(__name__)

app.secret_key = "compiler-project-secret-key"


def make_json_safe(value):

    if isinstance(value, set):
        return list(value)

    if isinstance(value, dict):
        return {
            key: make_json_safe(val)
            for key, val in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            make_json_safe(item)
            for item in value
        ]

    return value


@app.route("/", methods=["GET"])
def home():

    result = session.pop("analysis_result", None)

    if result:

        return render_template(
            "index.html",
            grammar_text=result["grammar_text"],
            input_string=result["input_string"],
            non_terminals=result["non_terminals"],
            terminals=result["terminals"],
            start_symbol=result["start_symbol"],
            productions=result["productions"],
            first_sets=result["first_sets"],
            follow_sets=result["follow_sets"],
            parsing_table=result["parsing_table"],
            ll1_conflict=result["ll1_conflict"],
            parse_result=result["parse_result"]
        )

    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    grammar_text = request.form["grammar"]
    input_string = request.form["input_string"]

    try:

        grammar = Grammar(grammar_text)

        grammar.parse()

        # Remove direct left recursion
        grammar.remove_direct_left_recursion()

        # Perform left factoring
        grammar.left_factor()

        # Calculate FIRST and FOLLOW sets
        first_sets = grammar.calculate_first_sets()

        follow_sets = grammar.calculate_follow_sets()

        # Build LL(1) parsing table
        try:

            parsing_table = grammar.build_parsing_table()

            ll1_conflict = None

        except ValueError as error:

            parsing_table = {}

            ll1_conflict = str(error)

        # Parse input only if grammar is LL(1)
        if ll1_conflict is None:

            parse_result = grammar.parse_input(
                input_string
            )

        else:

            parse_result = None

        result = {

            "grammar_text": grammar_text,
            "input_string": input_string,


            "non_terminals": grammar.non_terminals,

            "terminals": grammar.terminals,

            "start_symbol": grammar.start_symbol,

            "productions": grammar.productions,

            "first_sets": first_sets,

            "follow_sets": follow_sets,

            "parsing_table": parsing_table,

            "ll1_conflict": ll1_conflict,

            

            "parse_result": parse_result
        }

        session["analysis_result"] = make_json_safe(
            result
        )

        return redirect(
            url_for("home")
        )

    except ValueError as error:

        return render_template(
            "index.html",
            error=str(error)
        )


if __name__ == "__main__":
    app.run(debug=True)