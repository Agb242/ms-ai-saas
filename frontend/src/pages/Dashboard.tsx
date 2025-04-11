import { useQuery } from '@tanstack/react-query';
import {
  Grid,
  Paper,
  Typography,
  Box,
  CircularProgress,
} from '@mui/material';
import axios from 'axios';

const fetchDashboardData = async () => {
  const token = localStorage.getItem('token');
  const response = await axios.get('http://localhost:8000/tenants/me', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export default function Dashboard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: fetchDashboardData,
  });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Typography color="error">
        Une erreur est survenue lors du chargement des données
      </Typography>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Tableau de bord
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6} lg={4}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Informations du compte
            </Typography>
            <Typography variant="body1">
              Nom: {data.name}
            </Typography>
            <Typography variant="body1">
              Email: {data.email}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Configuration SMS
            </Typography>
            <Typography variant="body1">
              Numéro associé: {data.phone_number || 'Non configuré'}
            </Typography>
            <Typography variant="body1">
              Statut: {data.kannel_sid ? 'Actif' : 'Non configuré'}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Configuration IA
            </Typography>
            <Typography variant="body1">
              Clé API: {data.openrouter_key ? 'Configurée' : 'Non configurée'}
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
} 