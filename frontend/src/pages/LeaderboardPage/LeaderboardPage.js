import { useEffect } from "react";
import Leaderboard from "./components/Leaderboard/Leaderboard";
import { Box } from "@mui/material";
import PageHeader from "../../components/shared/PageHeader";
import Logo from "../../components/Logo/Logo";
import { useLeaderboardData } from "../../pages/LeaderboardPage/components/Leaderboard/hooks/useLeaderboardData";
import { useLeaderboard } from "../../pages/LeaderboardPage/components/Leaderboard/context/LeaderboardContext";

function LeaderboardPage() {
  const { data, isLoading, error } = useLeaderboardData();
  const { actions } = useLeaderboard();

  useEffect(() => {
    if (data) {
      actions.setModels(data);
    }
    actions.setLoading(isLoading);
    actions.setError(error);
  }, [data, isLoading, error, actions]);

  return (
    <Box
      sx={{
        ph: 2,
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Box
        sx={{ 
          display: "flex", 
          justifyContent: "center", 
          pt: 4,
          pb: 2,
          width: "100%",
          overflow: "hidden",
        }}
      >
        <Logo height="80px" />
      </Box>
      <PageHeader
        title="Open Financial LLM Leaderboard"
        subtitle={
          <>
            Benchmark for large language models in {" "}
            <span style={{ fontWeight: 600 }}>financial</span> domain {" "}
            across multiple languages and modalities
          </>
        }
      />
      <Leaderboard />
    </Box>
  );
}

export default LeaderboardPage;
