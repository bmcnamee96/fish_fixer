import { evaluateWaterQuality } from './rules.js';

export function normalizeCaseInput(payload = {}) {
  const get = (snakeKey, camelKey) => payload[snakeKey] ?? payload[camelKey] ?? null;
  return {
    waterType: get('water_type', 'waterType'),
    species: payload.species ?? null,
    symptoms: payload.symptoms ?? [],
    behavioralChanges: get('behavioral_changes', 'behavioralChanges'),
    pH: get('ph', 'pH'),
    ammonia: payload.ammonia ?? null,
    nitrite: payload.nitrite ?? null,
    dissolvedOxygen: get('dissolved_oxygen', 'dissolvedOxygen')
  };
}

export function buildAssessment(normalizedInput) {
  const alerts = evaluateWaterQuality(normalizedInput);
  return {
    likelyConditions: [
      {
        name: 'Water quality stress',
        confidence: alerts.length ? 'medium' : 'low'
      }
    ],
    alerts,
    nextSteps: [
      'Confirm test kit values with a second reading.',
      'Increase aeration and observe behavior over 24 hours.',
      'Quarantine symptomatic fish if signs worsen.'
    ],
    disclaimer:
      'This is informational guidance only and not a veterinary diagnosis.'
  };
}
