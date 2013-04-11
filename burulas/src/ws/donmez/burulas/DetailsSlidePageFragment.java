package ws.donmez.burulas;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import android.app.ListFragment;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

public class DetailsSlidePageFragment extends ListFragment {
    public static final String ARG_PAGE = "page";
    private int mPageNumber;

    private ArrayList<String> stopList;
    private ArrayList<ArrayList<String>> hourList;
    private int hourIndex;

    public static DetailsSlidePageFragment create(int pageNumber) {
        DetailsSlidePageFragment fragment = new DetailsSlidePageFragment();
        Bundle args = new Bundle();
        args.putInt(ARG_PAGE, pageNumber);
        fragment.setArguments(args);
        return fragment;
    }

    public DetailsSlidePageFragment() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setupHourList();
        mPageNumber = getArguments().getInt(ARG_PAGE);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState) {

        // Inflate the layout containing a title and body text.
        ViewGroup rootView = (ViewGroup) inflater
                .inflate(R.layout.fragment_details_slide_page, container, false);

        TextView tv = (TextView) rootView.findViewById(android.R.id.text1);

        setListAdapter(new ArrayAdapter<String>( getActivity(),
                                                 R.layout.custom_row_layout,
                                                 this.getForwardRoute()));

        setupListView();
        setHeader(tv);

        return rootView;
    }

    public int getPageNumber() {
        return mPageNumber;
    }

    public void setHeader(TextView tv) {
        switch (mPageNumber) {
            case 0:
                tv.setText("Forward Route");
                break;
            case 1:
                tv.setText("Backward Route");
                break;
            default:
                break;
        }

        if (mPageNumber > 1)
            setHourText(tv, mPageNumber);
    }

    public void setupListView() {
        switch (mPageNumber) {
            case 0:
                setListAdapter(new ArrayAdapter<String>( getActivity(),
                                                        R.layout.custom_row_layout,
                                                        this.getForwardRoute()));
                break;
            case 1:
                setListAdapter(new ArrayAdapter<String>( getActivity(),
                                                         R.layout.custom_row_layout,
                                                         this.getBackwardRoute()));
                break;
            default:
                break;
        }

        if (mPageNumber > 1) {
            setListAdapter(new ArrayAdapter<String>( getActivity(),
                                                     R.layout.custom_row_layout,
                                                     this.getHourList(mPageNumber)));
        }
    }

    private ArrayList<String> getForwardRoute() {
        ArrayList<String> forwardRoute = new ArrayList<String>(MainActivity.currentBus.forward);
        return forwardRoute;
    }

    private ArrayList<String> getBackwardRoute() {
        ArrayList<String> backwardRoute = new ArrayList<String>(MainActivity.currentBus.backward);
        return backwardRoute;
    }

    private void setupHourList() {
        stopList = new ArrayList<String>();
        hourList = new ArrayList<ArrayList<String>>();
        hourIndex = 0;

        HashMap<String, ArrayList<String>> busMap =
                new HashMap<String, ArrayList<String>>(MainActivity.currentBus.hours);
        List<String> keys = new ArrayList<String>(busMap.keySet());
        for (String key : keys) {
             hourList.add(new ArrayList<String>(MainActivity.currentBus.hours.get(key)));
             stopList.add(key);
        }
    }

    private void setHourText(TextView tv, int index) {
        tv.setText(stopList.get(index-2));
    }

    private ArrayList<String> getHourList(int index) {
        return hourList.get(index-2);
    }
}
