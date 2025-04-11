import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const Settings: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Paramètres
        </Typography>
        <Typography variant="body1">
          Configuration de l'application
        </Typography>
      </Paper>
    </Box>
  );
};

export default Settings; 