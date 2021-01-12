fetcher: ({url, method, data, config, headers}) => {
    config = config || {};
    config.headers = headers || {};

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