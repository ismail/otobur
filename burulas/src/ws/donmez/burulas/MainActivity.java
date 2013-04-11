package ws.donmez.burulas;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.zip.GZIPInputStream;

import javax.net.ssl.HttpsURLConnection;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.ListView;

public class MainActivity extends ListActivity {
    public static class Bus {
        ArrayList<String> backward;
        ArrayList<String> forward;
        LinkedHashMap<String, ArrayList<String>> hours;
        String url;
    }
    public static Bus currentBus;

    private static final int HTTP_CHUNK_SIZE = 8*1024;
    private static HashMap<String, Bus> busMap;
    private static String jsonURL = "https://raw.github.com/cartman/hackweek9/master/scripts/hours.json";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        new fetchScheduleTask().execute(jsonURL);
    }

    private class fetchScheduleTask extends AsyncTask<String, Void, ArrayList<String>> {

        private final ProgressDialog dialog = new ProgressDialog(MainActivity.this);

        @Override
        protected void onPreExecute() {
            this.dialog.setMessage("Fetching bus schedule...");
            this.dialog.show();
        }

        @Override
        protected ArrayList<String> doInBackground(String... urls) {
            ByteArrayOutputStream input = downloadSchedule(urls[0]);
            busMap = new HashMap<String, Bus>();
            ArrayList<String> busNames = new ArrayList<String>();

            try {
                JSONObject json = new JSONObject(input.toString());
                JSONArray keys = json.names();

                for (int i=0; i < keys.length(); ++i) {
                    String busName = keys.getString(i);
                    JSONObject root = json.getJSONObject(busName);
                    busNames.add(busName);

                    Bus bus = new Bus();

                    try {
                        ArrayList<String> backwardList = new ArrayList<String>();
                        JSONArray backwardArray = root.getJSONArray("backward");
                        for (int j=0; j < backwardArray.length(); ++j)
                            backwardList.add(backwardArray.getString(j));

                        bus.backward = backwardList;
                    } catch (JSONException e) {}

                    try {
                        ArrayList<String> forwardList = new ArrayList<String>();
                        JSONArray forwardArray = root.getJSONArray("forward");
                        for (int k=0; k < forwardArray.length(); ++k)
                            forwardList.add(forwardArray.getString(k));

                        bus.forward = forwardList;
                    } catch (JSONException e) { }

                    JSONObject hourArray = root.getJSONObject("hours");
                    JSONArray days = hourArray.names();
                    bus.hours = new LinkedHashMap<String, ArrayList<String>>();
                    for (int l=0; l < days.length(); ++l) {
                        String dayName = days.getString(l);
                        JSONArray hours = hourArray.getJSONArray(dayName);

                        ArrayList<String> hoursArray = new ArrayList<String>();
                        for (int m=0; m < hours.length(); ++m)
                            hoursArray.add(hours.getString(m));

                        bus.hours.put(dayName, hoursArray);
                    }

                    bus.url = root.getString("url");
                    busMap.put(busName, bus);

                }
            } catch(JSONException e) {
                Log.d("Burulas", e.toString());
            }

            Collections.sort(busNames);
            return busNames;
        }

        @Override
        protected void onPostExecute(ArrayList<String> busNames) {
            if(this.dialog.isShowing())
                this.dialog.dismiss();

            setListAdapter(new ArrayAdapter<String>(MainActivity.this,
                                                    R.layout.custom_row_layout,
                                                    busNames));
        }

        private ByteArrayOutputStream downloadSchedule(String address) {
            ByteArrayOutputStream result = new ByteArrayOutputStream();
            byte[] buffer = new byte[HTTP_CHUNK_SIZE];

            try {
                URL url =  new URL(address);
                HttpsURLConnection urlConnection = (HttpsURLConnection) url.openConnection();
                urlConnection.setRequestProperty("Accept-Encoding", "gzip, deflate");
                urlConnection.setRequestMethod("GET");

                InputStream inputStream = urlConnection.getInputStream();
                String contentEncoding = urlConnection.getHeaderField("Content-Encoding");

                if (contentEncoding != null && contentEncoding.equalsIgnoreCase("gzip")) {
                    inputStream = new GZIPInputStream(inputStream);
                }

                int length  = 0;
                while ( (length = inputStream.read(buffer)) > 0 ) {
                    result.write(buffer, 0, length);
                }
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

            return result;
        }
    }

    @Override
    protected void onListItemClick(ListView l, View v, int position, long id)
    {
        super.onListItemClick(l, v, position, id);
        Object o = this.getListAdapter().getItem(position);
        String busName = o.toString();
        currentBus = busMap.get(busName);
        Intent intent = new Intent(this, DetailsSlideActivity.class);

        startActivity(intent);
    }
}
