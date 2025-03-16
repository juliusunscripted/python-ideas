import itables.options as opt


def itables_use_basic_config(scrollY="300px"):
    # opt.paging = {
    #     "scrollY": "200px",
    #     "scrollCollapse": "true",
    #     "paging": "false",
    # }  # (default value)
    opt.columnDefs = [{"className": "dt-left", "targets": "_all"}]
    opt.paging = False

    # scrollX needed. otherwise wrong align left: https://github.com/mwouts/itables/issues/226#issuecomment-1925892259
    opt.scrollX = True
    opt.scrollCollapse = True
    opt.scrollY = scrollY
