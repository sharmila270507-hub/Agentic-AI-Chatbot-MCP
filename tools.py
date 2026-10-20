from ddgs import DDGS


def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""

    try:

        allowed = "0123456789+-*/(). "

        if not all(
            c in allowed
            for c in expression
        ):
            return "Invalid expression"

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception as e:

        return f"Calculation error: {e}"


def word_count(text: str) -> str:
    """Count words in text."""

    return str(
        len(text.split())
    )


def web_search(query: str) -> str:
    """Search the web and return concise search results."""

    try:

        results = DDGS().text(
            query,
            max_results=3
        )

        if not results:

            return "No search results found."


        output = []

        for i, result in enumerate(
            results,
            1
        ):

            title = result.get(
                "title",
                ""
            ).strip()

            body = result.get(
                "body",
                ""
            ).strip()

            url = result.get(
                "href",
                ""
            ).strip()


            # Limit long descriptions
            if len(body) > 300:

                body = body[:300] + "..."


            output.append(
                f"{i}. {title}\n"
                f"   {body}\n"
                f"   {url}"
            )


        return "\n\n".join(
            output
        )


    except Exception as e:

        return (
            f"Web search error: {e}"
        )
