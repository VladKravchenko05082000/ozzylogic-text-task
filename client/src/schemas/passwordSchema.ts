import { z } from "zod";

export const passwordRules = [
  { label: "At least 8 characters", test: (p: string) => p.length >= 8 },
  { label: "At most 20 characters", test: (p: string) => p.length <= 20 },
  { label: "At least one letter (a–z or A–Z)", test: (p: string) => /[A-Za-z]/.test(p) },
  { label: "At least one digit (0–9)", test: (p: string) => /[0-9]/.test(p) },
] as const;

export const passwordSchema = z
  .string({ error: "Password is required" })
  .min(8, { message: passwordRules[0].label })
  .max(20, { message: passwordRules[1].label })
  .regex(/[A-Za-z]/, { message: passwordRules[2].label })
  .regex(/[0-9]/, { message: passwordRules[3].label });
