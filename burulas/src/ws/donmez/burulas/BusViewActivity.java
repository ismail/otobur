package ws.donmez.burulas;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.LinkedHashMap;

import javax.net.ssl.HttpsURLConnection;

import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONException;

import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import ws.donmez.burulas.ForwardStopsActivity;

public class BusViewActivity extends ListActivity {
    private class Bus {
        ArrayList<String> backward;
        ArrayList<String> forward;
        LinkedHashMap<String, JSONArray> hours;
        String url;
    }

    private static LinkedHashMap<String, Bus> busMap;
    private static String jsonURL = "https://raw.github.com/cartman/hackweek9/master/scripts/hours.json";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        new fetchScheduleTask().execute(jsonURL);
    }

    private class fetchScheduleTask extends AsyncTask<String, Void, ArrayList<String>> {

        private final ProgressDialog dialog = new ProgressDialog(BusViewActivity.this);

        @Override
        protected void onPreExecute() {
            this.dialog.setMessage("Fetching bus schedule...");
            this.dialog.show();
        }

        @Override
        protected ArrayList<String> doInBackground(String... urls) {
            ByteArrayOutputStream input = downloadSchedule(urls[0]);
            busMap = new LinkedHashMap<String, Bus>();
            ArrayList<String> busNames = new ArrayList<String>();

            try {
                JSONObject json = new JSONObject(input.toString());
                JSONArray keys = json.names();

                for (int i=0; i < keys.length(); ++i) {
                    String entry = keys.getString(i);
                    JSONObject entries = json.getJSONObject(entry);
                    busNames.add(entry);

                    Bus bus = new Bus();

                    try {
                        ArrayList<String> backwardList = new ArrayList<String>();
                        JSONArray backwardArray = entries.getJSONArray("backward");
                        for (int j=0; j < backwardArray.length(); ++j)
                            backwardList.add(backwardArray.getString(j));

                        ArrayList<String> forwardList = new ArrayList<String>();
                        JSONArray forwardArray = entries.getJSONArray("forward");
                        for (int k=0; k < forwardArray.length(); ++k)
                            forwardList.add(forwardArray.getString(k));

                        bus.backward = backwardList;
                        bus.forward = forwardList;

                    } catch (JSONException e) { }

                    bus.url = entries.getString("url");
                    busMap.put(entry, bus);

                }
            } catch(JSONException e) {
            Log.d("Burulas", e.toString());
            }

            return busNames;
        }

        @Override
        protected void onPostExecute(ArrayList<String> busNames) {
            if(this.dialog.isShowing())
                this.dialog.dismiss();

            setListAdapter(new ArrayAdapter<String>(BusViewActivity.this,
                                                    android.R.layout.simple_list_item_1,
                                                    busNames));
        }

        private ByteArrayOutputStream downloadSchedule(String address) {
            ByteArrayOutputStream result = new ByteArrayOutputStream();
            byte[] buffer = new byte[4096];

            try {
                URL url =  new URL(address);
                HttpsURLConnection urlConnection = (HttpsURLConnection) url.openConnection();
                urlConnection.setRequestProperty("Accept-Encoding", "gzip, deflate");
                urlConnection.setRequestMethod("GET");

                InputStream inputStream = urlConnection.getInputStream();

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
        // Get the item that was clicked
        Object o = this.getListAdapter().getItem(position);
        String keyword = o.toString();
        Log.d("Burulas", keyword + " is selected!");
        Intent intent = new Intent(this, ForwardStopsActivity.class);
        intent.putExtra("ForwardStops", busMap.get(keyword).forward);
        startActivity(intent);
    }
}
