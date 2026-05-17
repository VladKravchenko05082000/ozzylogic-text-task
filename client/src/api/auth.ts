import client from "./client";

interface AuthDataPayloadInterface {
  email: string;
  password: string;
}

export const authApi = {
  register: (payload: AuthDataPayloadInterface) => client.post("/auth/register", payload),
  login: (payload: AuthDataPayloadInterface) => client.post("/auth/login", payload),
  refresh: (refresh_token: string) => client.post("/auth/refresh", { refresh_token }),
  logout: (refresh_token: string) => client.post("/auth/logout", { refresh_token }),
};
