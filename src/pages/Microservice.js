import React, { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';

import Map from 'ol/Map';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import View from 'ol/View';


function Microservice() {
  const { long } = useParams();
  const { lat } = useParams();
  const [map, setMap] = useState();
  const mapElement = useRef();
   
  useEffect(() => {
    
    // Create a tile layer 
    const tileLayer = new TileLayer({
      source: new OSM(),
    });
    
    // Create Map 
    const initialMap = new Map({
      target: mapElement.current,
      layers: [tileLayer],
      view: new View({
        projection: 'EPSG:4326',
        center: [long, lat],
        zoom: 9
      }),
    });
    
    // Save map 
    setMap(initialMap)
    
  }, []);
  
  return (
    <div className="microservice-page">
      <h3>Microservice Map</h3>
    
      {/* Microservice Map */}
      <div ref={mapElement} className="microservice-map">
      </div>
      
    </div>
  );
}

export default Microservice;