def define_env(env):
    @env.macro
    def realm(*realms):
        colors = {
            "server":   "#03A9F4",
            "client":   "#DEA909",
            "shared":   "#4CAF50",
            "database": "#FF3700",
            "api":      "#00FF99",
            "public":   "#00BCD4",
            "private":  "#FFA000",
        }
        badges = []
        for r in realms:
            color = colors.get(r.lower(), "#888")
            label = r.upper()
            badges.append(
                f'<span class="badge" style="background:{color};color:#fff">{label}</span>'
            )
        return " ".join(badges)

    @env.macro
    def state(*states):
        colors = {
            "private":    "#E53935",
            "public":   "#1E88E5",
        }
        badges = []
        for m in states:
            color = colors.get(m.lower(), "#888")
            badges.append(
                f'<span class="badge" style="background:{color};color:#fff">{m.upper()}</span>'
            )
        return " ".join(badges)

    @env.macro
    def method(*methods):
        colors = {
            "get":    "#4CAF50",
            "post":   "#1E88E5",
            "put":    "#FB8C00",
            "patch":  "#8E24AA",
            "delete": "#E53935",
        }
        badges = []
        for m in methods:
            color = colors.get(m.lower(), "#888")
            badges.append(
                f'<span class="badge" style="background:{color};color:#fff">{m.upper()}</span>'
            )
        return " ".join(badges)