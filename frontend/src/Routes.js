import React from 'react';
import { Switch, Redirect, Route } from 'react-router-dom';
import { DisplayPrices } from './views';

const Routes = () => {
  return (
    <Switch>
      <Redirect exact from='/' to='/search/prices' />
      <Route exact path='/search/prices'> <DisplayPrices /> </Route>
    </Switch>
  );
};

export default Routes;