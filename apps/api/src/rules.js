export function evaluateWaterQuality(observation) {
  const alerts = [];
  const waterType = (observation.waterType || '').toLowerCase();

  const ammonia = parseFloat(observation.ammonia);
  if (!Number.isNaN(ammonia) && ammonia > 0.25) {
    alerts.push('Ammonia is elevated and may be causing acute stress.');
  }

  const nitrite = parseFloat(observation.nitrite);
  if (!Number.isNaN(nitrite) && nitrite > 0.25) {
    alerts.push('Nitrite is elevated and can reduce oxygen transport.');
  }

  const dissolvedOxygen = parseFloat(observation.dissolvedOxygen);
  if (!Number.isNaN(dissolvedOxygen) && dissolvedOxygen < 5) {
    alerts.push('Dissolved oxygen appears low for many species.');
  }

  if (waterType === 'saltwater') {
    const ph = parseFloat(observation.pH);
    if (!Number.isNaN(ph) && (ph < 7.8 || ph > 8.5)) {
      alerts.push('pH appears out of typical saltwater range (7.8–8.5).');
    }
  }

  if (waterType === 'freshwater') {
    const ph = parseFloat(observation.pH);
    if (!Number.isNaN(ph) && (ph < 6 || ph > 8.2)) {
      alerts.push('pH appears out of common freshwater range (6.0–8.2).');
    }
  }

  return alerts;
}
