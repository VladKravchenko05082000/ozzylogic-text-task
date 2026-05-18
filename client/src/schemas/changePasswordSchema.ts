import { z } from "zod";
import { passwordSchema } from "./passwordSchema";

export const changePasswordSchema = z.object({
  current_password: passwordSchema,
  new_password: passwordSchema,
});

export type ChangePasswordForm = z.infer<typeof changePasswordSchema>;
