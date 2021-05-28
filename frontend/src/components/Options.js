import React, { Fragment } from "react";

const Options = ({ options, disabledLabel }) => {
  return (
    <Fragment>
      <option value="" defaultValue disabled>
        {disabledLabel}
      </option>
      {options.map((o) => (
        <option key={o} value={o}>
          {o}
        </option>
      ))}
    </Fragment>
  );
};

export default Options;
