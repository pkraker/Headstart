import React from "react";

import { useLocalizationContext } from "../../components/LocalizationProvider";

const Keywords = ({ children: text }) => {
  const localization = useLocalizationContext();

  return (
    // html template starts here
    <div id="list_keywords" style={{ display: "block" }}>
      <span className="keyword_tag">{localization.keywords}: </span>
      <span className="keywords highlightable">{text}</span>
    </div>
    // html template ends here
  );
};

export default Keywords;
