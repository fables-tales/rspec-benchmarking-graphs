def render_index(benchmark_groups):
    index_file = open("templates/index.html")
    template_contents = index_file.read()
    template_contents = template_contents.replace("$APP_LIST", generate_app_list(benchmark_groups))
    template_contents = template_contents.replace("$APP_PR_LIST", generate_app_pr_list(benchmark_groups))

    return template_contents


def render_pr_table(app, non_master_results, master_results):
    template_file = open("templates/pr.html")
    template_contents = template_file.read()
    template_contents = template_contents.replace("$MASTER_ROW", show_master_results(master_results))
    template_contents = template_contents.replace("$PULL_TABLE", show_pull_results(non_master_results))
    return template_contents


def generate_app_list(benchmark_groups):
    list_items = ["<li><a href='/app/" + x + "'>" + x + "</a></li>" for x in benchmark_groups]
    return "\n".join(list_items)


def show_master_results(master_results):
    time = master_results[0]
    deviation = master_results[1]
    return "<tr><td>" + str(time) + "</td><td>" + str(deviation) + "</td><td>master</td></tr>"


def show_pull_results(non_master_results):
    build = ""
    for time,deviation,branch in non_master_results:
        build += "<tr><td>" + str(time) + "</td><td>" + str(deviation) + "</td><td>" + branch + "</td></tr>\n"

    return build


def generate_app_pr_list(benchmark_groups):
    list_items = ["<li><a href='/app_pr/" + x + "'>" + x + "</li>" for x in benchmark_groups]
    return "\n".join(list_items)

