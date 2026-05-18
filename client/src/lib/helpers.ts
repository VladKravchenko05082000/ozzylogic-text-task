export function getToday() {
  return new Date().toISOString().slice(0, 10);
}

export function getDaysAgo(days: number) {
  const date = new Date();
  date.setDate(date.getDate() - days);
  return date.toISOString().slice(0, 10);
}
