import client from "./client";

type NearestBranchParamsType = {
  latitude: string;
  longitude: string;
  distance_limit?: string;
  limit?: number;
};

export const banksApi = {
  listBanks: () => client.get("/banks/banks-list"),
  getBank: (slug: string) =>
    client.get("/banks", {
      params: {
        slug,
      },
    }),
  getNearestBranches: (params: NearestBranchParamsType) =>
    client.get("banks/nearest-branches", { params }),
};
