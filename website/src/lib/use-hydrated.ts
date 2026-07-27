import { useSyncExternalStore } from "react";

const subscribe = () => () => {};

/**
 * `false` during server render and the first client render, `true` afterwards.
 *
 * Anything that depends on the resolved theme or on computed styles has to wait
 * for hydration, otherwise the markup React produces on the server will not
 * match the client.
 */
export function useHydrated(): boolean {
  return useSyncExternalStore(
    subscribe,
    () => true,
    () => false,
  );
}
