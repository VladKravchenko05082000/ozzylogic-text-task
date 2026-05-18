import client from "./client";

interface UserDataInterface {
  email: string;
  newsletter_enabled: boolean;
}

interface UpdateUserDataPayloadInterface extends UserDataInterface {}

interface ChangePasswordPayloadInterface {
  current_password: string;
  new_password: string;
}

export const userApi = {
  me: () => client.get("/user/me"),
  updateProfile: (payload: UpdateUserDataPayloadInterface) =>
    client.patch("/user/update-profile", payload),
  changePassword: (payload: ChangePasswordPayloadInterface) =>
    client.post("/user/change-password", payload),
};
