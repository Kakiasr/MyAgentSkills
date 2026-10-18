// Synthetic static-analysis fixture. Not code recovered from a commercial game.
export const goldChest = { keyCost: 2, coinReward: 8, actionCost: 1, goal: 13 };
export function openGold(state) {
  if (state.ended || state.actions < 1 || state.keys < 2) return { accepted: false, state };
  const next = { ...state, keys: state.keys - 2, coins: state.coins + 8, actions: state.actions - 1 };
  if (next.coins >= 13) { next.ended = true; next.result = 'won'; }
  else if (next.actions === 0) { next.ended = true; next.result = 'lost'; }
  return { accepted: true, state: next };
}
