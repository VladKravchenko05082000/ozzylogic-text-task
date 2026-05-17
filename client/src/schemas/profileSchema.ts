import { z } from "zod";

export const profileSchema = z.object({
  email: z.email(),
});

export type ProfileForm = z.infer<typeof profileSchema>;
