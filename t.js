// const access_token="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTYxMDQ1MDE1Mn0.tmYo0Av758Nkq3fi8fIRD2vFxkTukuG5WSD_gHaVjvc"
(function () {
        let amis = amisRequire('amis/embed');
        // 通过替换下面这个配置来生成不同页面
        let amisScoped = amis.embed('#root', {
            "type": "app",
            "api": null,
            "brandName": "\u9879\u76ee\u6d4b\u8bd5",
            "logo": null,
            "className": null,
            "header": null,
            "asideBefore": null,
            "asideAfter": null,
            "footer": null,
            "pages": [
                {
                "type": "route",
                "label": "fast_tmp example",
                "icon": null,
                "children": [
                    {
                    "type": "route",
                    "label": "fast_tmp_bk",
                    "icon": null,
                    "children": [{
                        "label": "fast_tmp",
                        "type": "page",
                        "icon": null,
                        "url": "/fast",
                        "schemaApi": "/fast/schema_api",
                        "rewrite": false,
                        "visable": true,
                        "redirect": null
                    }, {
                        "label": "admin",
                        "type": "page",
                        "icon": null,
                        "url": "/fast/admin",
                        "schemaApi": "/fast/admin/schema_api",
                        "rewrite": false,
                        "visable": true,
                        "redirect": null
                    }, {
                        "label": "base",
                        "type": "page",
                        "icon": null,
                        "url": "/fast/base",
                        "schemaApi": "/fast/base/schema_api",
                        "rewrite": false,
                        "visable": true,
                        "redirect": null
                    }]
                }, {
                    "type": "route",
                    "label": "example api",
                    "icon": null,
                    "children": [{
                        "label": "auth",
                        "type": "page",
                        "icon": null,
                        "url": "/example/auth",
                        "schemaApi": "/example/auth/schema_api",
                        "rewrite": false,
                        "visable": true,
                        "redirect": null
                    }]
                }, {
                    "label": "amis",
                    "type": "page",
                    "icon": null,
                    "url": "/amis",
                    "schemaApi": "/amis/schema_api",
                    "rewrite": false,
                    "visable": true,
                    "redirect": null
                }]
            }],
            "data": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTYxMDQ1MDE1Mn0.tmYo0Av758Nkq3fi8fIRD2vFxkTukuG5WSD_gHaVjvc",
                "token_type": "bearer"
            }
        }, {affixOffsetTop: 0}, {
            fetcher: ({url, method, data, config, header}) => {
                config = config || {};
                config.headers = headers || {};
                config.headers["Authorization"] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTYxMDQ1MDE1Mn0.tmYo0Av758Nkq3fi8fIRD2vFxkTukuG5WSD_gHaVjvc"
                if (config.cancelExecutor) {
                    config.cancelToken = new axios.CancelToken(config.cancelExecutor);
                }
                if (data && data instanceof FormData) {
                    // config.headers = config.headers || {};
                    // config.headers['Content-Type'] = 'multipart/form-data';
                } else if (
                    data &&
                    typeof data !== 'string' &&
                    !(data instanceof Blob) &&
                    !(data instanceof ArrayBuffer)
                ) {
                    data = JSON.stringify(data);
                    config.headers['Content-Type'] = 'application/json';
                }

                if (method !== 'post' && method !== 'put' && method !== 'patch') {
                    if (data) {
                        if (method === 'delete') {
                            config.data = data;
                        } else {
                            config.params = data;
                        }
                    }
                    return axios[method](url, config);
                }
                return axios[method](url, data, config);
            }
        })
    }
)();

