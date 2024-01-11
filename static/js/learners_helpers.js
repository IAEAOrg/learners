function findHiddenValueByPageId(obj, targetPageId) {
  for (const key in obj) {
    const currentObj = obj[key];

    if (currentObj.page_id === targetPageId) {
      return currentObj.hidden;
    }

    if (typeof currentObj.childs === "object") {
      const hiddenValue = findHiddenValueByPageId(
        currentObj.childs,
        targetPageId
      );
      if (hiddenValue !== undefined) {
        return hiddenValue;
      }
    }
  }
  return undefined;
}
