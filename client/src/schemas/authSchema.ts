import { z } from "zod";

export const authSchema = z.object({
  email: z.email(),

  password: z
    .string({ error: "Password is required" })
    .min(8, "Password must be between 8 and 20 characters")
    .max(20, "Password must be between 8 and 20 characters")
    .regex(/[A-Za-z]/, "Password must contain at least one letter (a-z or A-Z)")
    .regex(/[0-9]/, "Password must contain at least one number (0-9)"),
});

export type AuthForm = z.infer<typeof authSchema>;
