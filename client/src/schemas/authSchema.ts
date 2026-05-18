import { z } from "zod";
import { passwordSchema } from "./passwordSchema";

export const authSchema = z.object({
  email: z.email(),
  password: passwordSchema,
});

export type AuthForm = z.infer<typeof authSchema>;
