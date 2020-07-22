/**
 * This is where all actions are stored.
 */

export const zoomInFromMediator = () => ({
  type: "ZOOM_IN"
});

export const zoomOutFromMediator = () => ({
  type: "ZOOM_OUT"
});

export const zoomOut = (callback) => {
  return {type: "ZOOM_OUT", not_from_mediator: true};
};
