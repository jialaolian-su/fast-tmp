class ModelAdmin:
    methods = ["create", "delete", "update", "delete", "retrieve"]
    list_display = ("__str__",)
    list_display_links = ()
    list_filter = ()  # 过滤字段？
    list_select_related = False  # ？？
    list_per_page = 10  # list页面默认显示值
    list_max_show_all = 200  # list页面最大显示值
    list_editable = ()  # ？
    search_fields = ()  # 搜索字段
    date_hierarchy = None
    save_as = False
    save_as_continue = True
    save_on_top = False
    # 分页功能
    # paginator = Paginator
    preserve_filters = True
    inlines = []  # 内联显示？

    # Custom templates (designed to be over-ridden in subclasses)
    add_form_template = None
    change_form_template = None
    change_list_template = None
    delete_confirmation_template = None
    delete_selected_confirmation_template = None
    object_history_template = None
    popup_response_template = None

    # Actions
    actions = []
    # action对应的ser
    # action_form = helpers.ActionForm
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True

    # checks_class = ModelAdminChecks

    def get_route_conf(self):
        """
        获取路由配置，包括字段、枚举等信息
        :return:
        """

    @property
    def media(self):
        """
        返回静态文件
        :return:
        """
        return

    def get_ser_class(self):
        pass

    def get_ser(self):
        pass

    def get_queryset(self):
        pass
