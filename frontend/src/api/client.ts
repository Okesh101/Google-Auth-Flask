const BACKEND_URL = "http://127.0.0.1:5000";

interface OptionsProp {
    method?: string;
    headers?: Record<string, string>
}

async function apiFetch(url: string, options: OptionsProp = {}) {

    let accessToken = localStorage.getItem("access_token");

    let response = await fetch(`${BACKEND_URL}${url}`, {
        ...options,
        headers: {
            ...options.headers,
            Authorization: `Bearer ${accessToken}`
        },
        credentials: "include"
    });

    if (response.status === 401) {

        const refreshResponse = await fetch(
            `${BACKEND_URL}/api/v1/auth/refresh`,
            {
                method: "POST",
                credentials: "include"
            }
        );

        if (refreshResponse.ok) {

            const refreshData = await refreshResponse.json();

            localStorage.setItem(
                "access_token",
                refreshData.access_token
            );

            accessToken = refreshData.access_token;

            response = await fetch(`${BACKEND_URL}${url}`, {
                ...options,
                headers: {
                    ...options.headers,
                    Authorization: `Bearer ${accessToken}`
                },
                credentials: "include"
            });

        } else {

            localStorage.removeItem("access_token");

            window.location.href = "/";
        }
    }

    return response;
}

export default apiFetch;