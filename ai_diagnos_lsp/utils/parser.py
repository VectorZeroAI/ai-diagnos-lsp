from pathlib import Path


def parse_line(line: str, scope: List[str]) -> Path | None:
    line = line.strip()
    if "#" in line:
        if line.startswith("#"):
            return

        line = line.split("#")[0]
    
    tokens = line.split(" ")

    if tokens[0] not in ("from", "import"):
        return

    if tokens[0] == "from":
        import_path = tokens[1].split(".")

        if tokens [2] != "import":
            return
        
        if len(tokens) == 4:
            import_items = tokens[3]
        else:
            import_items: list[str] | str = []
            for i in tokens:
                if tokens.index(i) < 3:
                    continue
                uncrammed_token = i.split(",")
                for j in uncrammed_token:
                    j = j.strip()
                    import_items.append(j)
                

    if tokens[0] == "import":
        if "," in tokens[1]:
            for i in tokens:
                if tokens.index(i) == 0:
                    continue
                actual_tokens = i.split(",")
                for i in actual_tokens:
                    uncrammed_token = i.split(".")
                    for i in uncrammed_token:
                        import_path = ""
                        if uncrammed_token.index(i) != len(uncrammed_token):
                            if i == "":
                                import_path = import_path + "."
                                continue
                            import_path = import_path + "." + i
                        else:
                            import_items = i
            
        else:
            if len(tokens) > 2:
                for i in tokens:
                    if tokens.index(i) == 0:
                        continue
                    uncrammed_token = i.rstrip(",").split(".")
                    import_path = ""
                    for i in uncrammed_token:
                        if uncrammed_token.index(i) != len(uncrammed_token):
                            if i == "":
                                import_path = import_path + "."
                                continue
                            import_path = import_path + "." + i
                        else:
                            import_items = i
                            
            else:
                uncrammed_token = tokens[1].split(".")
                if len(uncrammed_token) == 0:
                    import_path = ""
                    import_items = uncrammed_token
                else:
                    import_path = ""
                    for i in uncrammed_token:
                        if uncrammed_token.index(i) != len(uncrammed_token):
                            if i == "":
                                import_path = import_path + "."
                                continue
                            import_path = import_path + "." + i
                        else:
                            import_items = i

