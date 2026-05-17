import { z } from "zod";

export const nearestBranchesSchema = z.object({
  lat: z
    .number({ error: "Latitude is required" })
    .min(-90, "Latitude must be between -90 and 90")
    .max(90, "Latitude must be between -90 and 90"),

  lng: z
    .number({ error: "Longitude is required" })
    .min(-180, "Longitude must be between -180 and 180")
    .max(180, "Longitude must be between -180 and 180"),

  // maxCount (бывший limit)
  maxCount: z
    .number()
    .int("Count must be an integer")
    .positive("Count must be greater than 0")
    .max(100, "Maximum 100 branches allowed")
    .optional()
    .default(10),

  // Дополнительный фильтр по расстоянию
  maxDistance: z
    .number()
    .positive("Max distance must be greater than 0")
    .max(100, "Maximum distance limit is 100 km")
    .optional()
    .default(10),
});

export type NearestBranchesInput = z.infer<typeof nearestBranchesSchema>;
