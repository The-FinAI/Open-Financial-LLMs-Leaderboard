import React from "react";
import { useNavigate, useSearchParams, useLocation } from "react-router-dom";
import { Box } from "@mui/material";
import { useLeaderboard } from "../../pages/LeaderboardPage/components/Leaderboard/context/LeaderboardContext";

/** Hide an image element if the src fails to load (e.g. file missing from /public). */
const handleImgError = (e) => {
  e.currentTarget.style.display = "none";
};

const LogoImage = ({ src, alt, maxHeight = 70, maxWidth = 200 }) => (
  <Box
    component="img"
    src={`${process.env.PUBLIC_URL}${src}`}
    alt={alt}
    onError={handleImgError}
    sx={{
      maxHeight,
      maxWidth,
      width: "auto",
      height: "auto",
      objectFit: "contain",
      flexShrink: 0,
      display: "block",
    }}
  />
);

const Logo = ({ height = "80px" }) => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const location = useLocation();
  const { actions } = useLeaderboard();

  const handleReset = () => {
    actions.resetAll();
    if (
      location.pathname !== "/" ||
      searchParams.toString() !== "" ||
      location.hash !== ""
    ) {
      window.history.replaceState(null, "", "/");
      navigate("/", { replace: true, state: { skipUrlSync: true } });
      setSearchParams({}, { replace: true, state: { skipUrlSync: true } });
    }
  };

  return (
    <Box
      onClick={handleReset}
      aria-label="Return to leaderboard home"
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === "Enter" && handleReset()}
      sx={{
        display: "flex",
        flexWrap: "wrap",
        alignItems: "center",
        justifyContent: "center",
        gap: { xs: 2, sm: 3, md: 4 },
        cursor: "pointer",
        px: 2,
        py: 1,
        transition: "opacity 0.2s ease",
        "&:hover": { opacity: 0.8 },
      }}
    >
      {/* Wide text logo — allow generous maxWidth */}
      <LogoImage src="/securefinailab.png" alt="SecureFinAI Lab" maxHeight={52} maxWidth={220} />

      {/* The Fin AI logo */}
      <LogoImage src="/logofinai.png" alt="The Fin AI" maxHeight={50} maxWidth={180} />

      {/* Very wide logo — allow extra width */}
      <LogoImage src="/nactemlogo.png" alt="NACTEM" maxHeight={44} maxWidth={200} />

      {/* Thin wide logo */}
      <LogoImage src="/archimedeslogo.png" alt="Archimedes" maxHeight={40} maxWidth={180} />

      {/* Square logo */}
      <LogoImage src="/airclogo.png" alt="AIRC" maxHeight={56} maxWidth={56} />
    </Box>
  );
};

export default Logo;
